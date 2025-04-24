"""
System monitoring module for the IdentiTwin system.

This module provides high-level system monitoring functionality including:
- Sensor data acquisition
- Data queue management
- System health monitoring
- Performance tracking
- Status reporting
- Error handling

Key Features:
- Multi-threaded data acquisition
- Real-time sensor monitoring
- Performance statistics tracking
- Automated sensor calibration
- Data buffering and management
- System status reporting
- Error recovery mechanisms

Classes:
    MonitoringSystem: Main class for system-level monitoring

The module serves as the central coordinator for the entire monitoring
system, managing all aspects of data acquisition and system operation.
"""

import os
import csv
import time
import threading
import traceback
import numpy as np
from collections import deque
from datetime import datetime
import logging
import queue
import matplotlib.pyplot as plt
import sys

from . import state
from . import processing_data, processing_analysis

class MonitoringSystem:
    """
    System-level monitoring class for the IdentiTwin system.
    Handles sensor setup, data acquisition, and system-level operations.
    """

    def __init__(self, config):
        """
        Initialize the monitoring system with the provided configuration.

        Args:
            config: Configuration object for the system.

        Returns:
            None

        Assumptions:
            - The configuration object (config) is properly initialized and contains necessary parameters.
        """
        self.config = config
        self.running = False
        self.data_queue = deque(maxlen=50000)
        self.acquisition_thread = None
        self.event_count = 0
        self.sensors_initialized = False
        self.last_status_time = 0
        self.status_interval = 2.0

        # Add counters for consecutive I/O errors per accelerometer
        self.accel_io_error_counts = [0] * (config.num_accelerometers if config.enable_accel else 0)
        self.accel_io_error_log_threshold = 100 # Log every 100 errors after the first

        self.performance_stats = {
            "accel_timestamps": deque(maxlen=50000),
            "lvdt_timestamps": deque(maxlen=50000),
            "accel_periods": deque(maxlen=50000),
            "lvdt_periods": deque(maxlen=50000),
            "last_accel_time": None,
            "last_lvdt_time": None,
            "sampling_rate_acceleration": 0.0,
            "sampling_rate_lvdt": 0.0,
            "accel_jitter": 0.0,
            "lvdt_jitter": 0.0,
        }

        self.last_lvdt_readings = []
        if (
            config.enable_lvdt
            and hasattr(config, "num_lvdts")
            and config.num_lvdts > 0
        ):
            self.last_lvdt_readings = [
                {"voltage": 0.0, "displacement": 0.0} for _ in range(config.num_lvdts)
            ]

        # Add display buffer for status updates
        self.display_buffer = {
            'accel_data': [],  # List of latest accelerometer readings
            'lvdt_data': [],   # List of latest LVDT readings
            'last_update': 0,  # Time of last buffer update
            'buffer_max_age': 0.5  # Maximum age of data in seconds
        }

    def setup_sensors(self):
        """
        Set up sensors based on the configuration.
        Initializes LVDTs, accelerometers, and LEDs.
        Relies on configurator methods for object creation.
        """
        print("\n--- Setting up sensors ---")
        self.sensors_initialized = False
        try:
            print("Initializing LEDs...")
            self.status_led, self.activity_led = self.config.initialize_leds()
            if self.status_led and self.activity_led:
                print("LEDs setup successful.")
            else:
                print("LEDs setup failed or skipped.")

            self.ads = None
            self.lvdt_channels = None
            if self.config.enable_lvdt:
                print("Initializing ADS1115 for LVDTs...")
                self.ads = self.config.create_ads1115()
                if self.ads:
                    print("ADS1115 setup successful.")
                    print("Initializing LVDT channels...")
                    self.lvdt_channels = self.config.create_lvdt_channels(self.ads)
                    if self.lvdt_channels:
                         print(f"LVDT channels setup successful ({len(self.lvdt_channels)} channels).")
                    else:
                         print("LVDT channels setup failed.")
                else:
                    print("ADS1115 setup failed.")

            self.accelerometers = None
            if self.config.enable_accel:
                print("Initializing Accelerometers (MPU6050)...")
                self.accelerometers = self.config.create_accelerometers()
                if self.accelerometers:
                    print(f"Accelerometers setup successful ({len(self.accelerometers)} sensors).")
                else:
                    print("Accelerometers setup failed.")

            # Final check for successful initialization based on config flags
            lvdt_ok = (not self.config.enable_lvdt) or (self.config.enable_lvdt and self.lvdt_channels)
            accel_ok = (not self.config.enable_accel) or (self.config.enable_accel and self.accelerometers)

            if lvdt_ok and accel_ok and (self.lvdt_channels or self.accelerometers):
                 self.sensors_initialized = True
                 print("--- Sensor setup completed successfully ---")
            else:
                 self.sensors_initialized = False
                 print("--- Sensor setup failed or incomplete ---", file=sys.stderr)
                 if self.config.enable_lvdt and not self.lvdt_channels:
                      print("  Reason: LVDT enabled but channels failed to initialize.", file=sys.stderr)
                 if self.config.enable_accel and not self.accelerometers:
                      print("  Reason: Accelerometer enabled but sensors failed to initialize.", file=sys.stderr)

        except Exception as e:
            print(f"Fatal error during sensor setup: {e}", file=sys.stderr)
            traceback.print_exc()
            self.sensors_initialized = False
            print("--- Sensor setup failed due to unexpected error ---", file=sys.stderr)

    def initialize_processing(self):
        """
        Initialize data processing and CSV file creation.
        Creates CSV files and plot variables necessary for data storage and visualization.

        Returns:
            None

        Assumptions:
            - Configuration object is properly initialized and contains necessary parameters
              such as output directory, number of LVDTs/accelerometers, sampling rates, etc.
        """
        self.csv_file_general = os.path.join(
            self.config.output_dir, "general_measurements.csv"
        )
        processing_data.initialize_general_csv(
            num_lvdts=self.config.num_lvdts if self.config.enable_lvdt else 0,
            num_accelerometers=self.config.num_accelerometers
            if self.config.enable_accel
            else 0,
            filename=self.csv_file_general,
        )
        if self.config.enable_lvdt:
            self.csv_file_displacement = os.path.join(
                self.config.output_dir, "displacements.csv"
            )
            processing_data.initialize_displacement_csv(
                filename=self.csv_file_displacement
            )
        if self.config.enable_accel:
            self.csv_file_acceleration = os.path.join(
                self.config.output_dir, "acceleration.csv"
            )
            processing_data.initialize_acceleration_csv(
                filename=self.csv_file_acceleration,
                num_accelerometers=self.config.num_accelerometers,
            )

    def start_monitoring(self):
        """
        Start the monitoring system.
        Initializes threads for data acquisition and starts hardware components.

        Returns:
            None

        Assumptions:
            - Sensors are initialized before calling this method.
            - Configuration includes necessary parameters.
        """
        if not self.sensors_initialized:
            print("Error: Sensors are not initialized. Call setup_sensors() first.")
            return

        if self.status_led:
            try:
                self.status_led.on()
            except Exception as e:
                print(f"Warning: Could not turn on status LED: {e}")

        self.running = True
        self.acquisition_thread = threading.Thread(
            target=self._data_acquisition_thread, daemon=True
        )
        self.acquisition_thread.start()

        if hasattr(self.config, "trigger_acceleration_threshold") or hasattr(
            self.config, "trigger_displacement_threshold"
        ):
            thresholds = {
                "acceleration": self.config.trigger_acceleration_threshold,
                "displacement": self.config.trigger_displacement_threshold,
                "detrigger_acceleration": self.config.detrigger_acceleration_threshold,
                "detrigger_displacement": self.config.detrigger_displacement_threshold,
                "pre_event_time": self.config.pre_event_time,
                "post_event_time": self.config.post_event_time,
                "min_event_duration": self.config.min_event_duration,
            }

            event_count_ref = [self.event_count]

            from .event_monitoring import EventMonitor
            self.event_monitor = EventMonitor(
                self.config, self.data_queue, thresholds, self.running, event_count_ref
            )
            self.event_thread = threading.Thread(
                target=self.event_monitor.event_monitoring_thread, daemon=True
            )
            self.event_thread.start()
            print("Event monitoring thread started.")

    def stop_monitoring(self):
        """
        Stop the monitoring system.
        Terminates threads and turns off LEDs.

        Returns:
            None
        """
        print("Stopping monitoring system...")
        self.running = False

        if self.acquisition_thread and self.acquisition_thread.is_alive():
            print("Waiting for acquisition thread to finish...")
            self.acquisition_thread.join(timeout=2.0)

        if (
            hasattr(self, "event_thread")
            and self.event_thread
            and self.event_thread.is_alive()
        ):
            print("Waiting for event thread to finish...")
            self.event_thread.join(timeout=2.0)

        if self.status_led:
            try:
                self.status_led.off()
            except Exception as e:
                print(f"Warning: Could not turn off status LED: {e}")
        if self.activity_led:
            try:
                self.activity_led.off()
            except Exception as e:
                print(f"Warning: Could not turn off activity LED: {e}")

        if hasattr(self, "event_monitor"):
            self.event_count = self.event_monitor.event_count_ref[0]

        print("Monitoring system stopped.")

    def cleanup(self):
        """
        Clean up resources used by the monitoring system.
        Closes plots and releases hardware resources.

        Returns:
            None
        """
        self.stop_monitoring()
        plt.close("all")
        print("Resources cleaned up.")

    def wait_for_completion(self):
        """
        Wait for monitoring to complete (blocks until interrupted).

        Returns:
            None
        """
        try:
            while self.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received. Stopping monitoring...")
            self.stop_monitoring()

    def _data_acquisition_thread(self):
        """
        Thread for data acquisition from sensors.
        Collects raw sensor data (acceleration/displacement) and enqueues for event handling.
        Applies calibration offsets/slopes from the config object. Handles read errors.
        """
        if not self.sensors_initialized:
             print("Error: Data acquisition thread cannot start, sensors not initialized.", file=sys.stderr)
             return

        try:
            accel_rate_target = self.config.sampling_rate_acceleration
            lvdt_rate_target = self.config.sampling_rate_lvdt

            accel_interval = 1.0 / accel_rate_target if accel_rate_target > 0 else float('inf')
            lvdt_interval = 1.0 / lvdt_rate_target if lvdt_rate_target > 0 else float('inf')

            stats_interval = 1.0

            accel_sample_count = 0
            lvdt_sample_count  = 0
            loop_start_time    = time.perf_counter()
            next_accel_time    = loop_start_time
            next_lvdt_time     = loop_start_time
            last_stats_update_time = loop_start_time

            last_accel_actual_time = None
            last_lvdt_actual_time = None

            print("\n--- Data acquisition thread started ---")

            while self.running:
                now = time.perf_counter()
                sensor_data_packet = None
                data_acquired = False

                if self.config.enable_accel and self.accelerometers and now >= next_accel_time:
                    # Add a mutex or lock for accelerometer access
                    self.accel_lock = threading.Lock()
                    with self.accel_lock:
                        target_accel_time = loop_start_time + accel_sample_count * accel_interval
                        sleep_needed = target_accel_time - now
                        if sleep_needed > 0:
                            self._precise_sleep(sleep_needed)
                        actual_accel_time = time.perf_counter()
                        expected_relative_time = accel_sample_count * accel_interval

                        if last_accel_actual_time is not None:
                            period = actual_accel_time - last_accel_actual_time
                            self.performance_stats["accel_periods"].append(period)
                        last_accel_actual_time = actual_accel_time

                        accel_data_list = []
                        for i, accel in enumerate(self.accelerometers):
                            try:
                                raw_data = accel.get_accel_data()
                                # Reset error counter on successful read
                                if i < len(self.accel_io_error_counts):
                                    if self.accel_io_error_counts[i] > 0:
                                        logging.info(f"Accelerometer {i+1} communication restored.")
                                    self.accel_io_error_counts[i] = 0

                                calibrated_data = raw_data
                                if i < len(self.config.accel_offsets):
                                    offsets = self.config.accel_offsets[i]
                                    if isinstance(offsets, dict):
                                        scaling_factor = offsets.get('scaling_factor', 1.0)
                                        calibrated_x = (raw_data['x'] + offsets.get('x', 0.0)) * scaling_factor
                                        calibrated_y = (raw_data['y'] + offsets.get('y', 0.0)) * scaling_factor
                                        calibrated_z = (raw_data['z'] + offsets.get('z', 0.0)) * scaling_factor
                                        calibrated_data = {'x': calibrated_x, 'y': calibrated_y, 'z': calibrated_z}
                                    else:
                                        print(f"Warning: Invalid calibration data structure for accelerometer {i+1}. Expected dict, got {type(offsets)}. Using raw data.", file=sys.stderr)
                                else:
                                    print(f"Warning: No calibration offset found for accelerometer {i+1}. Using raw data.", file=sys.stderr)

                                mag = np.sqrt(calibrated_data['x']**2 + calibrated_data['y']**2 + calibrated_data['z']**2)
                                calibrated_data['magnitude'] = mag
                                accel_data_list.append(calibrated_data)

                            except OSError as read_err:
                                if read_err.errno == 121: # Specific I/O error
                                    if i < len(self.accel_io_error_counts):
                                        self.accel_io_error_counts[i] += 1
                                        # Log less frequently
                                        if self.accel_io_error_counts[i] == 1 or \
                                           self.accel_io_error_counts[i] % self.accel_io_error_log_threshold == 0:
                                            logging.warning(f"I/O Error reading accelerometer {i+1} (Count: {self.accel_io_error_counts[i]}): {read_err}")
                                else: # Other OS errors
                                    logging.warning(f"Failed to read accelerometer {i+1}: {read_err}")
                                    if i < len(self.accel_io_error_counts): # Reset counter for other errors
                                        self.accel_io_error_counts[i] = 0
                                accel_data_list.append({'x': np.nan, 'y': np.nan, 'z': np.nan, 'magnitude': np.nan})
                            except Exception as e:
                                logging.error(f"Unexpected error processing accelerometer {i+1}: {e}", exc_info=True)
                                if i < len(self.accel_io_error_counts): # Reset counter for other errors
                                    self.accel_io_error_counts[i] = 0
                                accel_data_list.append({'x': np.nan, 'y': np.nan, 'z': np.nan, 'magnitude': np.nan})

                        timestamp = datetime.now()
                        sensor_data_packet = {
                            'timestamp': timestamp,
                            'expected_relative_time': expected_relative_time,
                            'sensor_type': 'accel',
                            'sensor_data': {'accel_data': accel_data_list}
                        }
                        accel_sample_count += 1
                        next_accel_time = loop_start_time + accel_sample_count * accel_interval
                        data_acquired = True

                elif self.config.enable_lvdt and self.lvdt_channels and now >= next_lvdt_time:
                    # Add similar timing logic as accelerometer
                    if last_lvdt_actual_time is not None:
                        period = now - last_lvdt_actual_time
                        self.performance_stats["lvdt_periods"].append(period)
                    last_lvdt_actual_time = now

                    # Add a mutex or lock for LVDT access
                    self.lvdt_lock = threading.Lock()
                    with self.lvdt_lock:
                        lvdt_data_list = []
                        for i, ch in enumerate(self.lvdt_channels):
                            try:
                                # Add delay between channel readings
                                if i > 0:
                                    time.sleep(0.001)  # 1ms delay between channels
                                    
                                raw_voltage = ch.voltage
                                
                                # Get calibration for this LVDT from config
                                if hasattr(self.config, 'lvdt_calibration') and i < len(self.config.lvdt_calibration):
                                    calib = self.config.lvdt_calibration[i]
                                    slope = calib.get('lvdt_slope', 19.86)  
                                    intercept = calib.get('lvdt_intercept', 0.0)
                                    
                                    # Calculate displacement using calibration
                                    disp = slope * raw_voltage + intercept
                                    
                                    lvdt_data_list.append({
                                        'voltage': raw_voltage,
                                        'displacement': disp
                                    })
                                    
                                    # Update last valid reading
                                    if i < len(self.last_lvdt_readings):
                                        self.last_lvdt_readings[i] = {
                                            'voltage': raw_voltage,
                                            'displacement': disp
                                        }
                                else:
                                    print(f"Warning: Missing calibration for LVDT {i+1}")
                                    lvdt_data_list.append({
                                        'voltage': raw_voltage,
                                        'displacement': 0.0
                                    })
                                    
                            except Exception as e:
                                print(f"Error reading LVDT {i+1}: {str(e)}", file=sys.stderr)
                                # Use last valid reading if available
                                if i < len(self.last_lvdt_readings):
                                    lvdt_data_list.append(self.last_lvdt_readings[i])
                                else:
                                    lvdt_data_list.append({'voltage': 0.0, 'displacement': 0.0})

                        timestamp = datetime.now()
                        expected_relative_time = lvdt_sample_count * lvdt_interval
                        sensor_data_packet = {
                            'timestamp': timestamp,
                            'expected_relative_time': expected_relative_time,
                            'sensor_type': 'lvdt',
                            'sensor_data': {'lvdt_data': lvdt_data_list}
                        }
                        lvdt_sample_count += 1
                        next_lvdt_time = loop_start_time + lvdt_sample_count * lvdt_interval
                        data_acquired = True

                if sensor_data_packet:
                    self.data_queue.append(sensor_data_packet)
                    # Update display buffer with fresh data
                    now = time.time()
                    if sensor_data_packet.get('sensor_type') == 'accel':
                        self.display_buffer['accel_data'] = sensor_data_packet.get('sensor_data', {}).get('accel_data', [])
                        self.display_buffer['last_update'] = now
                    elif sensor_data_packet.get('sensor_type') == 'lvdt':
                        self.display_buffer['lvdt_data'] = sensor_data_packet.get('sensor_data', {}).get('lvdt_data', [])
                        self.display_buffer['last_update'] = now
                    if self.activity_led:
                        try:
                            self.activity_led.blink(on_time=0.01, off_time=0.01, n=1, background=True)
                        except Exception:
                            pass

                if now - last_stats_update_time >= stats_interval:
                    self._update_performance_stats(
                        self.performance_stats["accel_periods"],
                        self.performance_stats["lvdt_periods"]
                    )
                    self._print_status(sensor_data_packet if sensor_data_packet else {})
                    last_stats_update_time = now

                if not data_acquired:
                    earliest_next_time = float('inf')
                    if self.config.enable_accel and accel_interval != float('inf'):
                        earliest_next_time = min(earliest_next_time, next_accel_time)
                    if self.config.enable_lvdt and lvdt_interval != float('inf'):
                        earliest_next_time = min(earliest_next_time, next_lvdt_time)

                    if earliest_next_time != float('inf'):
                        sleep_duration = earliest_next_time - time.perf_counter() - 0.001
                        if sleep_duration > 0.0001:
                            self._precise_sleep(sleep_duration)
                    else:
                        time.sleep(0.01)

        except Exception as e:
            print(f"Fatal error in data acquisition thread: {e}", file=sys.stderr)
            traceback.print_exc()
        finally:
            print("--- Data acquisition thread finished ---")

    def _precise_sleep(self, sleep_time):
        """
        Implements precise sleep using a combination of sleep and active waiting.

        Args:
            sleep_time: Time in seconds to sleep.

        Returns:
            None
        """
        if sleep_time <= 0:
            return

        if (sleep_time < 0.001): #
            target = time.perf_counter() + sleep_time
            while time.perf_counter() < target:
                pass
            return

        time.sleep(sleep_time - 0.0005)
        target = time.perf_counter() + 0.0005
        while time.perf_counter() < target:
            pass

    def _update_performance_stats(self, recent_accel_periods, recent_lvdt_periods):
        """
        Calculate performance statistics using provided recent periods.

        Args:
            recent_accel_periods: Deque of recent accelerometer periods.
            recent_lvdt_periods: Deque of recent LVDT periods.

        Returns:
            None
        """
        if len(recent_accel_periods) > 1:
            periods_np = np.array(recent_accel_periods)
            mean_period = np.mean(periods_np)
            std_dev_period = np.std(periods_np)
            self.performance_stats["sampling_rate_acceleration"] = 1.0 / mean_period if mean_period > 0 else 0.0
            self.performance_stats["accel_jitter"] = std_dev_period * 1000.0
        else:
            self.performance_stats["sampling_rate_acceleration"] = 0.0
            self.performance_stats["accel_jitter"] = 0.0

        if len(recent_lvdt_periods) > 1:
            periods_np = np.array(recent_lvdt_periods)
            mean_period = np.mean(periods_np)
            std_dev_period = np.std(periods_np)
            self.performance_stats["sampling_rate_lvdt"] = 1.0 / mean_period if mean_period > 0 else 0.0
            self.performance_stats["lvdt_jitter"] = std_dev_period * 1000.0
        else:
            self.performance_stats["sampling_rate_lvdt"] = 0.0
            self.performance_stats["lvdt_jitter"] = 0.0

    def _print_status(self, sensor_data):
        """
        Print current system status information.

        Args:
            sensor_data: A dictionary containing sensor data from the latest acquisition.

        Returns:
            None
        """
        print("\n============================ System Status Update =============================\n")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")

        print("Performance:")
        if self.config.enable_accel:
            accel_rate_measured = self.performance_stats.get("sampling_rate_acceleration", 0.0)
            accel_jitter_measured = self.performance_stats.get("accel_jitter", 0.0)
            print(f"  Accel Rate: {accel_rate_measured:.2f} Hz (Target: {self.config.sampling_rate_acceleration:.1f} Hz)")
            print(f"  Accel Jitter: {accel_jitter_measured:.2f} ms")

        if self.config.enable_lvdt:
            lvdt_rate_measured = self.performance_stats.get("sampling_rate_lvdt", 0.0)
            lvdt_jitter_measured = self.performance_stats.get("lvdt_jitter", 0.0)
            print(f"  LVDT Rate: {lvdt_rate_measured:.2f} Hz (Target: {self.config.sampling_rate_lvdt:.1f} Hz)")
            print(f"  LVDT Jitter: {lvdt_jitter_measured:.2f} ms")

        if self.config.enable_lvdt:
            print("\nLVDT Status:")
            for i, reading in enumerate(self.last_lvdt_readings):
                disp = reading.get('displacement', float('nan'))
                volt = reading.get('voltage', float('nan'))
                print(f"  LVDT{i+1}: {disp:.3f}mm ({volt:.3f}V)")

        if self.config.enable_accel:
            print("\nAccelerometer Status:")
            now = time.time()
            buffer_age = now - self.display_buffer['last_update']
            
            if buffer_age <= self.display_buffer['buffer_max_age']:
                accel_data = self.display_buffer['accel_data']
                if accel_data:
                    for i, accel in enumerate(accel_data):
                        if isinstance(accel, dict):
                            x = accel.get('x', 0.0)
                            y = accel.get('y', 0.0)
                            z = accel.get('z', 0.0)
                            mag = np.sqrt(x*x + y*y + z*z)
                            print(f"  Accel{i+1}: X={x:.3f} Y={y:.3f} Z={z:.3f} (Mag: {mag:.3f}) m/s^2")
                else:
                    print("  Waiting for accelerometer data...")
            else:
                print("  Data not updated in the last 500ms")

        event_count = self.event_monitor.event_count_ref[0] if hasattr(self, 'event_monitor') else 0
        state_event_count = state.get_event_variable("event_count", 0)

        current_event_count = max(event_count, state_event_count)
        print(f"\nEvents detected: {current_event_count}")

        if event_count != state_event_count:
            state.set_event_variable("event_count", event_count)

        is_recording = state.get_event_variable("is_event_recording", False)
        formatted_time = "Not recording"
        if is_recording:
            last_trigger = state.get_event_variable("last_trigger_time", 0)
            if last_trigger > 0:
                elapsed = time.time() - last_trigger
                formatted_time = f"Recording event... ({elapsed:.1f}s elapsed)"
        print(f"Recording Status: {formatted_time}")

        if hasattr(self, "event_monitor"):
            avg_accel = self.event_monitor.moving_avg_accel
            avg_disp = self.event_monitor.moving_avg_disp
            detrig_accel = self.config.detrigger_acceleration_threshold
            detrig_disp = self.config.detrigger_displacement_threshold
            print(f"Acceleration Moving Average: {avg_accel:.3f} (detrigger: {detrig_accel:.3f}m/s^2)")
            print(f"Displacement Moving Average: {avg_disp:.3f} (detrigger: {detrig_disp:.3f}mm)")

        print("\n===============================================================================")
        print("====================== `Ctrl + C` to finish monitoring ========================\n \n")

    def _format_elapsed_time(self, elapsed_seconds):
        """
        Format elapsed time in human-readable format.

        Args:
            elapsed_seconds: Time in seconds.

        Returns:
            Formatted time string.
        """
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"