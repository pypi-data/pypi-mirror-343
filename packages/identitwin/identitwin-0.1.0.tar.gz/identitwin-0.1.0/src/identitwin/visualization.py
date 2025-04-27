"""Visualization module for real-time data display in IdentiTwin.

Uses Dash/Plotly for efficient real-time plotting of sensor data.
Includes virtual LED indicators within each tab to show system status
(running/stopped) and recording status (event recording active/inactive).

Attributes:
    pio.templates.default (str): Default Plotly template for styling.
    PALETTE (list): Color palette for plots.
    MAX_POINTS (int): Maximum number of data points to display in time-series plots.
    FFT_BUFFER_SIZE (int): Size of the buffer for FFT calculations (power of 2).
    FFT_BUFFERS (dict): Dictionary storing FFT data buffers per sensor.
    LVDT_BUFFER (dict): Dictionary storing real-time LVDT data buffers.
    ACC_BUFFER (dict): Dictionary storing real-time accelerometer data buffers.
    SENSOR_COLORS (list): Custom color set for sensor lines in plots.
    COMPONENT_COLORS (dict): Base colors for accelerometer components (x, y, z).
    LED_STYLE_BASE (dict): Base CSS style for LED indicators.
    LED_STYLE_OFF (dict): CSS style for LED when off.
    LED_STYLE_STATUS_ON (dict): CSS style for status LED when on.
    LED_STYLE_RECORDING_ON (dict): CSS style for recording LED when on.
"""

import dash
from dash import dcc, html, ALL
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import threading
import plotly.io as pio
import random
import time
from collections import deque
import numpy as np
from .processing_analysis import calculate_fft
import logging
import socket
import webbrowser
from . import state

# Set template for consistent styling
pio.templates.default = "plotly_dark"

PALETTE = ['#A97830','#296F8C', '#BCBEC0', '#000000']

MAX_POINTS = 3000        
# Añadir buffer FFT potencia de 2
FFT_BUFFER_SIZE = 1024  # potencia de 2 >= muestras necesarias
FFT_BUFFERS = {}        # sensor_index -> {'magnitude','x','y','z'} -> deque

# Real‐time sampling buffers
LVDT_BUFFER = {}     # sensor_index -> deque of (t, displacement)
ACC_BUFFER = {}      # sensor_index -> deque of (t, magnitude, x, y, z)

# Custom color set for sensor lines
SENSOR_COLORS = [
    '#FF5733', '#33FF57', '#3357FF', '#FF33A8', 
    '#33FFF5', '#F533FF', '#FF8C33', '#8CFF33',
    '#338CFF', '#FF338C', '#33FFC4', '#C433FF'
]

# add base colors per component
COMPONENT_COLORS = {
    'x': '#FF5733',
    'y': '#33FF57',
    'z': '#3357FF'
}

# --- LED Styles ---
LED_STYLE_BASE = {
    'width': '20px',
    'height': '20px',
    'borderRadius': '50%',
    'display': 'inline-block',
    'marginLeft': '10px',
    'border': '2px solid grey', # Grey ring
    'verticalAlign': 'middle',
}

LED_STYLE_OFF = {**LED_STYLE_BASE, 'backgroundColor': 'black'}
LED_STYLE_STATUS_ON = {**LED_STYLE_BASE, 'backgroundColor': 'lime'}
LED_STYLE_RECORDING_ON = {**LED_STYLE_BASE, 'backgroundColor': 'blue'}


def _shade_color(hex_color, dark=False):
    """Darkens a hex color code by a factor.

    Args:
        hex_color (str): The hex color code (e.g., '#FF5733').
        dark (bool): If True, darken the color by a factor of 0.6.
                     Otherwise, return the original color.

    Returns:
        str: The modified (or original) hex color code.
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i+2],16) for i in (0,2,4))
    factor = 0.6 if dark else 1.0
    r, g, b = [max(0, min(255,int(c*factor))) for c in (r,g,b)]
    return f'#{r:02X}{g:02X}{b:02X}'

def _create_led_indicators(tab_value):
    """Creates the HTML structure for status and recording LEDs for a specific tab.

    Args:
        tab_value (str): The identifier for the tab (e.g., 'lvdt-tab', 'accel-tab').

    Returns:
        dash.html.Div: A Div element containing the LED indicators and labels.
    """
    return html.Div([
        html.Span("System Status:", style={'verticalAlign': 'middle'}),
        # Use dictionary IDs for pattern matching
        html.Div(id={'type': 'status-led', 'tab': tab_value}, style=LED_STYLE_OFF),
        html.Span("Recording Status:", style={'marginLeft': '20px', 'verticalAlign': 'middle'}),
        html.Div(id={'type': 'recording-led', 'tab': tab_value}, style=LED_STYLE_OFF),
    ], style={'marginTop': '10px', 'marginBottom': '10px', 'textAlign': 'center'}) # Center LEDs

def create_dashboard(system_monitor):
    """Creates and configures the Dash application layout.

    Builds the dashboard structure with tabs for different sensor types
    (LVDT, Accelerometer, FFT) based on the system configuration.
    Includes LED indicators in each tab. Defines callbacks for updating
    plots and LEDs based on interval triggers and user selections.

    Args:
        system_monitor (MonitoringSystem): The main monitoring system instance,
            containing the configuration and state information.

    Returns:
        dash.Dash: The configured Dash application instance.
    """
    app = dash.Dash(__name__, suppress_callback_exceptions=True) # Suppress exceptions for pattern matching if needed initially

    # Build tabs based on config options
    if system_monitor.config.enable_plots:
        default_tab = None
        tabs_children = []

        if system_monitor.config.enable_plot_displacement:
            tab_value = "displacements"
            if default_tab is None:
                default_tab = tab_value
            tabs_children.append(dcc.Tab(label='Displacements', value=tab_value, children=[
                _create_led_indicators(tab_value), # ADDED LEDs here with unique ID
                html.H3("Displacements", style={'textAlign': 'left', 'color': PALETTE[1]}),
                html.Div([
                    html.Label("Select LVDT:"),
                    dcc.Dropdown(
                    id='lvdt-selector',
                    options=[{'label': 'All', 'value': 'all'}] +
                            [{'label': f'LVDT {i+1}', 'value': str(i)} 
                             for i in range(system_monitor.config.num_lvdts)],
                    value='all',
                    multi=True,
                    style={'color': 'black', 'backgroundColor': PALETTE[2]}
                ),
                ], style={'width': '50%', 'margin': 'auto', 'marginBottom': '40px'}),                
                dcc.Graph(id='lvdt-plot') # Keep original graph ID
            ]))

        if system_monitor.config.enable_accel_plots:
            tab_value = "accelerations"
            if default_tab is None:
                default_tab = tab_value
            tabs_children.append(dcc.Tab(label='Accelerations', value=tab_value, children=[
                _create_led_indicators(tab_value), # ADDED LEDs here with unique ID
                html.H3("Accelerations", style={'textAlign': 'left', 'color': PALETTE[1]}),
                html.Div([
                    html.Label("Select Accelerometer:"),
                    dcc.Dropdown(
                        id='acc-selector',
                        options=[{'label': 'All', 'value': 'all'}] +
                                [{'label': f'ACC {i+1}', 'value': str(i)} 
                                 for i in range(system_monitor.config.num_accelerometers)],
                        value='all',
                        multi=True,
                        style={'color': 'black', 'backgroundColor': PALETTE[2]}
                    ),
                ], style={'width': '50%', 'margin': 'auto', 'marginBottom': '40px'}),
                
                html.Div([   # componente ahora multi-select
                    html.Label("Select Component:"),
                    dcc.Dropdown(
                        id='acc-component-selector',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'X', 'value': 'x'},
                            {'label': 'Y', 'value': 'y'},
                            {'label': 'Z', 'value': 'z'}
                        ],
                        value=['all'],
                        multi=True,
                        style={'color': 'black', 'backgroundColor': PALETTE[2]}
                    ),
                ], style={'width': '50%', 'margin': 'auto', 'marginBottom': '40px'}),
                dcc.Graph(id='acceleration-plot') # Keep original graph ID
            ]))

        if system_monitor.config.enable_fft_plots:
            tab_value = "fft"
            if default_tab is None:
                default_tab = tab_value
            tabs_children.append(dcc.Tab(label='FFT Analysis', value=tab_value, children=[
                _create_led_indicators(tab_value), # ADDED LEDs here with unique ID
                html.H3("FFT Analysis", style={'textAlign': 'Left', 'color': PALETTE[1]}),
                html.Div([
                    html.Label("Select Accelerometer:"),
                    dcc.Dropdown(
                        id='fft-acc-selector',
                        options=[{'label':'All','value':'all'}] +
                                [{'label':f'ACC {i+1}','value':str(i)} 
                                 for i in range(system_monitor.config.num_accelerometers)],
                        value='all', multi=True,
                        style={'color':'black','backgroundColor':PALETTE[2]}
                    )
                ], style={'width':'50%','margin':'auto','marginBottom':'40px'}),
                html.Div([
                    html.Label("Select Component:"),
                    dcc.Dropdown(
                        id='fft-component-selector',
                        options=[
                            {'label':'All','value':'all'},
                            {'label':'X','value':'x'},
                            {'label':'Y','value':'y'},
                            {'label':'Z','value':'z'}
                        ],
                        value=['all'],            # default to all => x,y,z
                        multi=True,
                        style={'color':'black','backgroundColor':PALETTE[2]}
                    )
                ], style={'width':'50%','margin':'auto','marginBottom':'40px'}),
                dcc.Graph(id='fft-plot') # Keep original graph ID
            ]))

        layout_children = [
            html.H1("IdentiTwin Real-Time Monitoring",
                    style={'textAlign': 'center', 'color': PALETTE[0]}),
            html.Img(src="https://github.com/estructuraPy/IdentiTwin/raw/main/identitwin.png",
                     style={'width': '100px', 'margin': 'auto', 'display': 'block'}),
            dcc.Tabs(id='tabs', value=default_tab, children=tabs_children),
            dcc.Interval(
                id='interval-component',
                interval=int(1000/system_monitor.config.plot_refresh_rate),  # ms per update
                n_intervals=0
            )
        ]
    else:
        # Fallback layout if enable_plots is False
        layout_children = [html.H1("IdentiTwin", style={'textAlign': 'center'})]
    
    app.layout = html.Div(layout_children)
    
    @app.callback(
        Output('lvdt-plot', 'figure'),
        [Input('interval-component', 'n_intervals'),
         Input('lvdt-selector', 'value')]
    )
    def update_lvdt_graph(n, selected_lvdts):
        # if no data sampled yet
        if not LVDT_BUFFER:
            return go.Figure()

        fig = go.Figure()

        # normalize selection
        if selected_lvdts is None:
            selected_lvdts = ['all']
        elif not isinstance(selected_lvdts, list):
            selected_lvdts = [selected_lvdts]
        show_all = 'all' in selected_lvdts
        sel_idxs = [int(i) for i in selected_lvdts if i != 'all']

        # plot from buffer
        for i, buf in LVDT_BUFFER.items():
            if show_all or i in sel_idxs:
                xs, ys = zip(*buf) if buf else ([], [])
                fig.add_trace(go.Scatter(
                    x=list(xs),
                    y=list(ys),
                    mode='lines',
                    line={'color': SENSOR_COLORS[i % len(SENSOR_COLORS)]},
                    name=f'LVDT {i+1}'
                ))

        # Calculate offset for relative time display
        offset = 0
        for sensor in LVDT_BUFFER.values():
            if sensor:
                t_end = sensor[-1][0]
                offset = t_end - system_monitor.config.window_duration if t_end >= system_monitor.config.window_duration else 0
                break
        xr = [0, system_monitor.config.window_duration]
        # Adjust each trace to show relative times
        for trace in fig.data:
            trace.x = [x - offset for x in trace.x]
        
        # Calculate dynamic range for Y axis using only currently visible points
        y_vals = []
        for trace in fig.data:
            # Filter values where the corresponding x is in [0, window_duration]
            filtered_y = [y for x, y in zip(trace.x, trace.y) if 0 <= x <= xr[1]]
            y_vals.extend(filtered_y)
        if y_vals:
            y_min = min(y_vals)
            y_max = max(y_vals)
            padding = (y_max - y_min) * 0.1 if y_max != y_min else 1
            dyn_y_range = [y_min - padding, y_max + padding]
        else:
            dyn_y_range = [-50, 50]
        
        # Add trigger and detrigger lines
        if hasattr(system_monitor.config, 'trigger_displacement_threshold'):
            trigger_threshold_disp = system_monitor.config.trigger_displacement_threshold
            fig.add_trace(go.Scatter(x=xr, y=[trigger_threshold_disp, trigger_threshold_disp], mode='lines', line=dict(color='orange', dash='dash'), name='Trigger'))
            fig.add_trace(go.Scatter(x=xr, y=[-trigger_threshold_disp, -trigger_threshold_disp], mode='lines', line=dict(color='orange', dash='dash'), name='Trigger'))
        if hasattr(system_monitor.config, 'detrigger_displacement_threshold'):
            detrigger_threshold_disp = system_monitor.config.detrigger_displacement_threshold
            fig.add_trace(go.Scatter(x=xr, y=[detrigger_threshold_disp, detrigger_threshold_disp], mode='lines', line=dict(color='purple', dash='dash'), name='Detrigger'))
            fig.add_trace(go.Scatter(x=xr, y=[-detrigger_threshold_disp, -detrigger_threshold_disp], mode='lines', line=dict(color='purple', dash='dash'), name='Detrigger'))

        fig.update_layout(
            xaxis={'title': 'Time (s)', 'range': xr, 'color': PALETTE[3]},
            yaxis={'title': 'Displacement', 'range': dyn_y_range, 'color': PALETTE[3]},
            height=375,
            margin=dict(l=40, r=40, t=60, b=40),
            paper_bgcolor=PALETTE[2],
            plot_bgcolor=PALETTE[2],
            font={'color': PALETTE[3]},
            showlegend=True,
            legend={'bgcolor': 'white'}
        )
        return fig

    @app.callback(
        Output('acceleration-plot', 'figure'),
        [Input('interval-component', 'n_intervals'),
         Input('acc-selector', 'value'),
         Input('acc-component-selector', 'value')]
    )
    def update_acceleration_graph(n, selected_accs, selected_comps):
        if not ACC_BUFFER:
            return go.Figure()

        fig = go.Figure()
        # sensor filtering
        if selected_accs is None:
            selected_accs = ['all']
        elif not isinstance(selected_accs, list):
            selected_accs = [selected_accs]
        show_all = 'all' in selected_accs
        sel_idxs = [int(i) for i in selected_accs if i != 'all']

        # component filtering: only x, y, z
        if not selected_comps or 'all' in selected_comps:
            comps = ['x','y','z']
        else:
            comps = [c for c in selected_comps if c in COMPONENT_COLORS]

        comp_map = {'x':2, 'y':3, 'z':4}

        for i, buf in ACC_BUFFER.items():
            if show_all or i in sel_idxs:
                buf_copy = list(buf)  # create a copy to prevent mutation during iteration
                times = [entry[0] for entry in buf_copy]
                for comp in comps:
                    idx = comp_map.get(comp)
                    vals = [entry[idx] for entry in buf_copy]
                    base = COMPONENT_COLORS[comp]
                    color = _shade_color(base, dark=(i % 2 == 1))
                    fig.add_trace(go.Scatter(
                        x=times, y=vals, mode='lines',
                        line={'color': color}, name=f'ACC {i+1} {comp.upper()}'
                    ))

        # Calculate offset for relative time display
        offset = 0
        for sensor in ACC_BUFFER.values():
            if sensor:
                t_end = sensor[-1][0]
                offset = t_end - system_monitor.config.window_duration if t_end >= system_monitor.config.window_duration else 0
                break
        xr = [0, system_monitor.config.window_duration]
        
        for trace in fig.data:
            trace.x = [x - offset for x in trace.x]
        
        # Calculate dynamic range for Y axis using only currently visible points
        y_vals = []
        for trace in fig.data:
            filtered_y = [y for x, y in zip(trace.x, trace.y) if 0 <= x <= xr[1]]
            y_vals.extend(filtered_y)
        if y_vals:
            y_min = min(y_vals)
            y_max = max(y_vals)
            padding = (y_max - y_min) * 0.1 if y_max != y_min else 1
            dyn_y_range = [y_min - padding, y_max + padding]
        else:
            dyn_y_range = [-50, 50]
        
        # Add trigger and detrigger lines
        if hasattr(system_monitor.config, 'trigger_acceleration_threshold'):
            trigger_threshold_accel = system_monitor.config.trigger_acceleration_threshold
            fig.add_trace(go.Scatter(x=xr, y=[trigger_threshold_accel, trigger_threshold_accel], mode='lines', line=dict(color='orange', dash='dash'), name='Trigger'))
            fig.add_trace(go.Scatter(x=xr, y=[-trigger_threshold_accel, -trigger_threshold_accel], mode='lines', line=dict(color='orange', dash='dash'), name='Trigger'))
        if hasattr(system_monitor.config, 'detrigger_acceleration_threshold'):
            detrigger_threshold_accel = system_monitor.config.detrigger_acceleration_threshold
            fig.add_trace(go.Scatter(x=xr, y=[detrigger_threshold_accel, detrigger_threshold_accel], mode='lines', line=dict(color='purple', dash='dash'), name='Detrigger'))
            fig.add_trace(go.Scatter(x=xr, y=[-detrigger_threshold_accel, -detrigger_threshold_accel], mode='lines', line=dict(color='purple', dash='dash'), name='Detrigger'))

        fig.update_layout(
            xaxis={'title': 'Time (s)', 'range': xr, 'color': PALETTE[3]},
            yaxis={'title': 'Acceleration', 'range': dyn_y_range, 'color': PALETTE[3]},
            height=375,
            margin=dict(l=40, r=40, t=60, b=40),
            paper_bgcolor=PALETTE[2],
            plot_bgcolor=PALETTE[2],
            font={'color': PALETTE[3]},
            showlegend=True,
            legend={'bgcolor': 'white'}
        )
        return fig

    # New FFT callback if FFT tab is enabled
    if system_monitor.config.enable_fft_plots:
        @app.callback(
            Output('fft-plot', 'figure'),
            [
                Input('interval-component', 'n_intervals'),
                Input('fft-acc-selector', 'value'),
                Input('fft-component-selector', 'value')
            ]
        )
        def update_fft_graph(n, selected_accs, selected_comps):
            # normalizar selección de sensores
            if selected_accs is None or not isinstance(selected_accs, list):
                selected_accs = [selected_accs] if selected_accs else ['all']
            show_all = 'all' in selected_accs
            sel_idxs = [int(i) for i in selected_accs if i!='all']

            # preparar figura
            fig = go.Figure()

            # normalizar selección de componentes
            # component filtering: only x, y, z
            if not selected_comps or 'all' in selected_comps:
                comps = ['x','y','z']
            else:
                comps = [c for c in selected_comps if c in COMPONENT_COLORS]

            for i, bufs in FFT_BUFFERS.items():
                if show_all or i in sel_idxs:
                    # build full XYZ arrays once
                    data_x = np.array(bufs.get('x', []))
                    data_y = np.array(bufs.get('y', []))
                    data_z = np.array(bufs.get('z', []))
                    if not all(len(arr) == FFT_BUFFER_SIZE for arr in (data_x, data_y, data_z)):
                        continue
                    freq, fft_x, fft_y, fft_z = calculate_fft(
                        {'x': data_x, 'y': data_y, 'z': data_z},
                        system_monitor.config.sampling_rate_acceleration
                    )
                    for comp in comps:
                        spec = {'x': fft_x, 'y': fft_y, 'z': fft_z}[comp]
                        base_color = COMPONENT_COLORS[comp]
                        color = _shade_color(base_color, dark=(i % 2 == 1))
                        fig.add_trace(go.Scatter(
                            x=freq, y=spec,
                            name=f'ACC {i+1} {comp.upper()}',
                            line={'color': color}
                        ))

            # ensure we have a valid max_freq (fall back to Nyquist or 1.0)
            try:
                max_freq = float(freq.max())
            except Exception:
                max_freq = system_monitor.config.sampling_rate_acceleration / 2

            fig.update_layout(
                title='FFT Accelerometers',
                xaxis={
                    'title':'Frequency (Hz)',
                    'color': PALETTE[3],
                    'range': [0.5, max_freq]
                },
                yaxis={'title':'Amplitude', 'color': PALETTE[3]},
                paper_bgcolor=PALETTE[2],
                plot_bgcolor=PALETTE[2],
                font={'color':PALETTE[3]},
                height=375,
                margin={'l':40,'r':40,'t':80,'b':40},
                showlegend=True
            )
            return fig

    # --- Modified Callbacks for LEDs using Pattern Matching ---
    @app.callback(
        Output({'type': 'status-led', 'tab': ALL}, 'style'), # Match all status LEDs
        [Input('interval-component', 'n_intervals')]
    )
    def update_status_led_style(n):
        """Update the status LED color based on system running state."""
        is_running = state.get_system_variable('system_running', False)
        style = LED_STYLE_STATUS_ON if is_running else LED_STYLE_OFF
        # Return a list of styles, one for each matched LED
        # Check if callback_context is available (might not be on initial load)
        num_leds = 1
        if dash.callback_context.outputs_list:
             num_leds = len(dash.callback_context.outputs_list)
        return [style] * num_leds

    @app.callback(
        Output({'type': 'recording-led', 'tab': ALL}, 'style'), # Match all recording LEDs
        [Input('interval-component', 'n_intervals')]
    )
    def update_recording_led_style(n):
        """Update the recording LED color based on event recording state (with blinking)."""
        is_recording = state.get_event_variable('is_event_recording', False)
        style = LED_STYLE_OFF # Default to OFF

        if is_recording:
            blink_cycle_duration = 0.7
            blink_on_duration = 0.3
            current_time = time.time()
            time_in_cycle = current_time % blink_cycle_duration
            if time_in_cycle < blink_on_duration:
                style = LED_STYLE_RECORDING_ON 
            else:
                style = LED_STYLE_OFF
        else:
            style = LED_STYLE_OFF

        # Return a list of styles, one for each matched LED
        # Check if callback_context is available
        num_leds = 1
        if dash.callback_context.outputs_list:
             num_leds = len(dash.callback_context.outputs_list)
        return [style] * num_leds
    
    return app

def run_dashboard(system_monitor):
    """Initializes and runs the Dash dashboard application.

    Args:
        system_monitor (MonitoringSystem): The main monitoring system instance.
    """
    app = create_dashboard(system_monitor)

    def run():
        import logging, socket, webbrowser, time as _t
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

        # Automatic IP detection
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            external_ip = s.getsockname()[0]
            s.close()
        except:
            external_ip = "127.0.0.1"

        dashboard_url = f"http://{external_ip}:8050"
        print(f"\nAccess dashboard at: {dashboard_url}\n")

        # --- start sampling threads ---
        start_time = time.time()

        def lvdt_sampler():
            period = 1.0 / system_monitor.config.sampling_rate_lvdt
            while True:
                buf = LVDT_BUFFER
                disp = system_monitor.display_buffer.get('lvdt_data', [])
                t = time.time() - start_time
                for i, s in enumerate(disp):
                    if i not in buf:
                        buf[i] = deque(maxlen=MAX_POINTS)
                    buf[i].append((t, s.get('displacement', 0)))
                _t.sleep(period)

        def acc_sampler():
            period = 1.0 / system_monitor.config.sampling_rate_acceleration
            while True:
                buf = ACC_BUFFER
                data = system_monitor.display_buffer.get('accel_data', [])
                t = time.time() - start_time
                for i, s in enumerate(data):
                    if i not in buf:
                        buf[i] = deque(maxlen=MAX_POINTS)
                    buf[i].append((
                        t,
                        s.get('magnitude', 0),
                        s.get('x', 0),
                        s.get('y', 0),
                        s.get('z', 0)
                    ))
                    # inicializar FFT_BUFFERS para sensor i
                    if i not in FFT_BUFFERS:
                        FFT_BUFFERS[i] = {
                            'magnitude': deque([0.0]*FFT_BUFFER_SIZE, maxlen=FFT_BUFFER_SIZE),
                            'x': deque([0.0]*FFT_BUFFER_SIZE, maxlen=FFT_BUFFER_SIZE),
                            'y': deque([0.0]*FFT_BUFFER_SIZE, maxlen=FFT_BUFFER_SIZE),
                            'z': deque([0.0]*FFT_BUFFER_SIZE, maxlen=FFT_BUFFER_SIZE)
                        }
                    # actualizar FFT de cada componente
                    FFT_BUFFERS[i]['magnitude'].append(s.get('magnitude',0))
                    FFT_BUFFERS[i]['x'].append(s.get('x',0))
                    FFT_BUFFERS[i]['y'].append(s.get('y',0))
                    FFT_BUFFERS[i]['z'].append(s.get('z',0))
                _t.sleep(period)

        threading.Thread(target=lvdt_sampler, daemon=True).start()
        threading.Thread(target=acc_sampler, daemon=True).start()
        # --- end sampling threads ---

        # Attempt to open browser (will silently fail if headless)
        def open_browser():
            _t.sleep(1.5)
            try:
                webbrowser.open_new(dashboard_url)
            except:
                pass

        threading.Thread(target=open_browser, daemon=True).start()

        try:
            app.run(debug=False, host='0.0.0.0', port=8050)
        except Exception as e:
            print(f"ERROR starting dashboard: {e}")
            print("Try accessing at http://127.0.0.1:8050 instead\n")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread
