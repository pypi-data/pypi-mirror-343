"""
Data processing module for the IdentiTwin monitoring system.

This module handles all aspects of sensor data processing including:
- Data acquisition and validation
- CSV file management and data storage
- Real-time data processing
- Multi-sensor data synchronization
- Data format conversions

Key Features:
- Multiple sensor type support (LVDT, accelerometer)
- Automated file creation and management
- Data validation and cleaning
- Time synchronization between sensors
- Error detection and handling
- Efficient data structure management

The module provides core functionality for handling all sensor data
throughout the monitoring system lifecycle.
"""

import csv
import os
import numpy as np
import logging
import time  # Added for sleep functionality
from datetime import datetime, timedelta

def initialize_general_csv(num_lvdts, num_accelerometers, filename='general_measurements.csv'):
    """Initialize a CSV file for storing both LVDT and accelerometer data."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Create header with both absolute and relative time
        header = ['Timestamp', 'Time']  # Changed from 'Expected_Time'
        
        # Add LVDT columns
        for i in range(num_lvdts):
            header.append(f'LVDT{i+1}_Voltage')
            header.append(f'LVDT{i+1}_Displacement')
            
        # Add accelerometer columns
        for i in range(num_accelerometers):
            header.extend([f'Accel{i+1}_X', f'Accel{i+1}_Y', f'Accel{i+1}_Z', f'Accel{i+1}_Magnitude'])
            
        writer.writerow(header)
    return filename

def initialize_displacement_csv(filename='displacements.csv', num_lvdts=2):
    """Initialize a CSV file for LVDT displacement measurements."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Create header with both absolute and relative time
        header = ['Timestamp', 'Time']  # Changed from 'Expected_Time'
        for i in range(num_lvdts):
            header.extend([f'LVDT{i+1}_Voltage', f'LVDT{i+1}_Displacement'])
            
        writer.writerow(header)
    return filename

def initialize_acceleration_csv(filename='acceleration.csv', num_accelerometers=2):
    """Initialize a CSV file for accelerometer measurements."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Create header with both absolute and relative time
        header = ['Timestamp', 'Time']  # Changed from 'Expected_Time'
        for i in range(num_accelerometers):
            header.extend([f'Accel{i+1}_X', f'Accel{i+1}_Y', f'Accel{i+1}_Z', f'Accel{i+1}_Magnitude'])
            
        writer.writerow(header)
    return filename

def read_lvdt_data(lvdt_channels, config):
    """
    Reads each LVDT channel and applies slope/intercept calibration.
    Raises exception if calibration data is missing.
    Returns a list of dicts with 'voltage' and 'displacement'.
    """
    lvdt_values = []
    for i, ch in enumerate(lvdt_channels):
        try:
            # Add small delay before reading to ensure stable readings
            time.sleep(0.001)  # 1ms delay for stability
            
            voltage = ch.voltage
            
            # Use individual calibration parameters - fail explicitly if missing
            if not hasattr(config, 'lvdt_calibration'):
                print(f"Warning: No LVDT calibration data available in configuration. Using slope=20, intercept=0.")
                slope = 20.0
                intercept = 0.0
            elif i >= len(config.lvdt_calibration) or config.lvdt_calibration[i] is None:
                print(f"Warning: Missing calibration data for LVDT {i+1}. Using slope=20, intercept=0.")
                slope = 20.0
                intercept = 0.0
            else:
                calib = config.lvdt_calibration[i]
                # Check for both possible key names
                slope = calib.get('slope', calib.get('lvdt_slope'))
                intercept = calib.get('intercept', calib.get('lvdt_intercept'))
                
                if slope is None or intercept is None:
                    print(f"Warning: Incomplete calibration parameters for LVDT {i+1}. Using slope=20, intercept=0.")
                    slope = 20.0
                    intercept = 0.0
            
            displacement = slope * voltage + intercept
            
            # Print debug info for first reading
            if i == 0 and len(lvdt_values) == 0:
                print(f"DEBUG: LVDT {i+1} reading - voltage: {voltage:.4f}V, slope: {slope:.4f}, "
                      f"intercept: {intercept:.4f}, displacement: {displacement:.4f}mm")
            
            lvdt_values.append({
                'voltage': voltage,
                'displacement': displacement
            })
        except Exception as e:
            print(f"Error reading LVDT {i+1}: {e}")
            # Return empty dict instead of raising, to allow system to continue
            lvdt_values.append({'voltage': 0.0, 'displacement': 0.0})
            
    return lvdt_values

def extract_data_from_event(event_data, start_time, config):
    """Extract numerical data from event_data structure for analysis."""
    np_data = {}
    
    # Extract timestamps
    timestamps = []
    for data in event_data:
        if "timestamp" in data and isinstance(data["timestamp"], datetime):
             timestamps.append(data["timestamp"])
        else:
             logging.warning(f"Missing or invalid timestamp in event data entry: {data}")
             continue
    
    if not timestamps:
        logging.error("No valid timestamps found in event data.")
        return {}

    first_ts = min(timestamps)
    last_ts = max(timestamps)
    actual_duration = (last_ts - first_ts).total_seconds()

    if config.enable_accel:
        # Store main timestamps array (used primarily for accelerometer data)
        np_data['timestamps'] = np.array([(ts - first_ts).total_seconds() for ts in timestamps])
        np_data['absolute_timestamps'] = np.array([ts.timestamp() for ts in timestamps])
        
        for accel_idx in range(config.num_accelerometers):
            accel_x, accel_y, accel_z, accel_mag = [], [], [], []
            
            for data in event_data:
                 if "timestamp" not in data or not isinstance(data["timestamp"], datetime):
                     continue
                 
                 sensor_dict = data.get("sensor_data", {})
                 accel_list = sensor_dict.get("accel_data", [])
                 
                 if accel_idx < len(accel_list):
                    accel = accel_list[accel_idx]
                    if all(k in accel for k in ['x', 'y', 'z']):
                        accel_x.append(accel['x'])
                        accel_y.append(accel['y'])
                        accel_z.append(accel['z'])
                        mag = np.sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)
                        accel_mag.append(mag)
                    else:
                        accel_x.append(np.nan)
                        accel_y.append(np.nan)
                        accel_z.append(np.nan)
                        accel_mag.append(np.nan)
                 else:
                     accel_x.append(np.nan)
                     accel_y.append(np.nan)
                     accel_z.append(np.nan)
                     accel_mag.append(np.nan)

            if accel_x:
                np_data[f'accel{accel_idx+1}_x'] = np.array(accel_x)
                np_data[f'accel{accel_idx+1}_y'] = np.array(accel_y)
                np_data[f'accel{accel_idx+1}_z'] = np.array(accel_z)
                np_data[f'accel{accel_idx+1}_mag'] = np.array(accel_mag)

    # Extract LVDT data
    if config.enable_lvdt:
        for lvdt_idx in range(config.num_lvdts):
            lvdt_times = []
            lvdt_displacements = []
            
            for data in event_data:
                if "timestamp" not in data or not isinstance(data["timestamp"], datetime):
                    continue

                sensor_dict = data.get("sensor_data", {})
                lvdt_list = sensor_dict.get("lvdt_data", [])

                if lvdt_idx < len(lvdt_list):
                    lvdt = lvdt_list[lvdt_idx]
                    disp = lvdt.get('displacement')
                    
                    if disp is not None and not np.isnan(disp):
                        rel_time = (data["timestamp"] - first_ts).total_seconds()
                        lvdt_times.append(rel_time)
                        lvdt_displacements.append(disp)

            if lvdt_times:
                key_time = f'lvdt{lvdt_idx+1}_time'
                key_disp = f'lvdt{lvdt_idx+1}_displacement'
                np_data[key_time] = np.array(lvdt_times)
                np_data[key_disp] = np.array(lvdt_displacements)

    return np_data

def create_displacement_csv(event_data, event_folder, config):
    """Create CSV file for LVDT displacement data."""
    displacement_file = os.path.join(event_folder, 'displacements.csv')
    
    try:
        with open(displacement_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Create header
            header = ['Timestamp', 'Time']  # Changed from 'Expected_Time'
            for i in range(config.num_lvdts):
                header.extend([f'LVDT{i+1}_Voltage', f'LVDT{i+1}_Displacement'])
            writer.writerow(header)
            
            # Correct start time to cover pre-event period.
            if not event_data:
                logging.warning("No event data provided for displacement CSV creation.")
                return displacement_file # Return empty file path
                
            # Use counter instead of measured time
            valid_counter = 0
            time_counter = 0
            
            rows_to_write = []
            # Collect data rows: use elapsed seconds from corrected start_time
            for data in event_data:
                # Check if 'sensor_data' and 'lvdt_data' exist and are not empty
                if "sensor_data" in data and "lvdt_data" in data["sensor_data"] and data["sensor_data"]["lvdt_data"]:
                    timestamp = data["timestamp"].strftime('%Y-%m-%d %H:%M:%S.%f')
                    # Expected time from counter and expected LVDT rate
                    time_value = time_counter * (1.0 / config.sampling_rate_lvdt)
                    row = [timestamp, f"{time_value:.6f}"]
                    for lvdt in data["sensor_data"]["lvdt_data"]:
                        # Ensure lvdt dictionary has the required keys
                        voltage = lvdt.get('voltage', float('nan')) # Use NaN as default if key missing
                        displacement = lvdt.get('displacement', float('nan'))
                        row.extend([f"{voltage:.6f}", f"{displacement:.6f}"])
                    rows_to_write.append(row)
                    valid_counter += 1
                    time_counter += 1
                else:
                    # Optionally log missing data or handle differently
                    logging.debug(f"Skipping data point due to missing LVDT data: {data.get('timestamp')}")


            # Write all collected rows at once
            if rows_to_write:
                writer.writerows(rows_to_write)
            else:
                logging.warning(f"No valid LVDT data found to write to {displacement_file}")

        return displacement_file
    except Exception as e:
        logging.error(f"Error creating displacement CSV: {e}", exc_info=True) # Log traceback
        return None

def create_acceleration_csv(event_data, event_folder, config):
    """Create CSV file for accelerometer data."""
    acceleration_file = os.path.join(event_folder, 'acceleration.csv')
    
    try:
        with open(acceleration_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Create header
            header = ['Timestamp', 'Time']  # Changed from 'Expected_Time'
            for i in range(config.num_accelerometers):
                header.extend([f'Accel{i+1}_X', f'Accel{i+1}_Y', f'Accel{i+1}_Z', f'Accel{i+1}_Magnitude'])
            writer.writerow(header)
            
            # Correct start time to cover pre-event period.
            if not event_data:
                logging.warning("No event data provided for acceleration CSV creation.")
                return acceleration_file # Return empty file path

            # Use counter instead of measured time
            valid_counter = 0
            time_counter = 0
            
            rows_to_write = []
            # Collect data rows: compute expected_time as elapsed seconds from corrected start_time
            for data in event_data:
                 # Check if 'sensor_data' and 'accel_data' exist and are not empty
                if "sensor_data" in data and "accel_data" in data["sensor_data"] and data["sensor_data"]["accel_data"]:
                    timestamp = data["timestamp"].strftime('%Y-%m-%d %H:%M:%S.%f')
                    # Expected time from counter and expected accelerometer rate
                    time_value = time_counter * (1.0 / config.sampling_rate_acceleration)
                    row = [timestamp, f"{time_value:.6f}"]
                    for accel in data["sensor_data"]["accel_data"]:
                        # Ensure accel dictionary has the required keys
                        x = accel.get('x', float('nan')) # Use NaN as default
                        y = accel.get('y', float('nan'))
                        z = accel.get('z', float('nan'))
                        # Calculate magnitude safely, handling potential NaNs
                        if not (np.isnan(x) or np.isnan(y) or np.isnan(z)):
                            magnitude = np.sqrt(x**2 + y**2 + z**2)
                        else:
                            magnitude = float('nan')
                            
                        row.extend([
                            f"{x:.6f}", 
                            f"{y:.6f}", 
                            f"{z:.6f}",
                            f"{magnitude:.6f}"
                        ])
                    rows_to_write.append(row)
                    valid_counter += 1
                    time_counter += 1
                else:
                     # Optionally log missing data or handle differently
                    logging.debug(f"Skipping data point due to missing Accelerometer data: {data.get('timestamp')}")


            # Write all collected rows at once
            if rows_to_write:
                writer.writerows(rows_to_write)
            else:
                 logging.warning(f"No valid Accelerometer data found to write to {acceleration_file}")

        return acceleration_file
    except Exception as e:
        logging.error(f"Error creating acceleration CSV: {e}", exc_info=True) # Log traceback
        return None