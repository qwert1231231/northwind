# Northwind Drone Navigation Library

**Version 1.1.2**

A comprehensive Python library for autonomous drone navigation and control systems, featuring AI-powered decision making, obstacle avoidance, real-time stability control, and advanced PWM motor speed control for ESP32/Arduino/drone hardware.

## Features

### 1. Navigation (Powerful Brain)
- `set_destination(lat, lon)` - Set navigation destination coordinates
- `calculate_route(start, end)` - Calculate optimal flight route
- `update_position()` - Update current drone position from sensors

### 2. Obstacle Handling (Critical)
- `detect_obstacle(sensor_data)` - Detect obstacles using sensor data
- `avoid_obstacle(direction)` - Execute obstacle avoidance maneuvers
- `recalculate_path()` - Recalculate path around detected obstacles

### 3. Stability / Correction (Real Drone Behavior)
- `correct_drift(gps_error)` - Correct GPS positioning drift
- `adjust_altitude(wind_data)` - Adjust altitude based on wind conditions
- `hold_position()` - Maintain stable hover position

### 4. Mission Control
- `start_mission()` - Begin autonomous mission
- `pause_mission()` - Pause current mission execution
- `return_home()` - Return to home position safely

### 5. Simple AI Decision Layer
- `choose_action(state)` - Choose optimal action based on current state
- `predict_next_move()` - Predict next optimal move using AI

### 6. Data Logging (For Learning + Cloud)
- `log_flight_data()` - Log flight telemetry and sensor data
- `export_data()` - Export logged data to JSON files
- `send_to_cloud()` - Upload data to cloud storage for analysis

## Installation

Install the latest release from PyPI:

```bash
pip install --upgrade northwind
```

Install the current repository version from GitHub:

```bash
pip install --upgrade git+https://github.com/qwert1231231/northwind.git
```

Or clone and install locally:

```bash
git clone https://github.com/qwert1231231/northwind.git
cd northwind
pip install -e .
```

## Quick Start

```python
import northwind

# Set destination coordinates
northwind.set_destination(37.7749, -122.4194)  # San Francisco

# Start autonomous mission
northwind.start_mission()

# Hardware motor control
northwind.set_hardware_device('esp32')
northwind.set_motor_speed(75)  # percent of full PWM range
northwind.ramp_motor_speed(90, step=10, delay=0.1)
status = northwind.get_motor_status()
print(status)

# AI decision making
action = northwind.choose_action('normal')
next_move = northwind.predict_next_move()

# Log flight data
northwind.log_flight_data()
northwind.export_data()
```

## Motor Speed Control

Northwind 1.1.2 introduces PWM-based motor speed control for embedded hardware platforms.
Supported device profiles:

- `esp32` — ESP32 PWM driver profile
- `arduino` — Arduino PWM driver profile
- `drone` — Generic drone ESC PWM profile

Use `set_hardware_device(...)` to choose the device type, then control speed with `set_motor_speed(...)` or `set_motor_speed_pwm(...)`.

## Requirements

- Python 3.8+
- GPS/IMU sensors (for real drone integration)
- Cloud storage account (optional, for data upload)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Repository

- GitHub: [https://github.com/qwert1231231/northwind](https://github.com/qwert1231231/northwind)
- PyPI: [https://pypi.org/project/northwind/](https://pypi.org/project/northwind/)