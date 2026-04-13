# Northwind Drone Navigation Library

**Version 1.3.0**

A comprehensive drone control library with **REAL HARDWARE SUPPORT** for Raspberry Pi, ESP32, Arduino, and Pico. Includes simulation mode for testing and learning.

## Real Hardware Support (v1.3.0+)

Northwind now controls **ACTUAL HARDWARE** drones with real PWM motors, sensors, and telemetry:

### Supported Platforms
- **Raspberry Pi** — GPIO PWM, I2C sensors, real telemetry
- **ESP32** — WiFi, PWM motors, analog sensors, real control
- **Arduino/Arduino Pico** — Serial communication, PWM motor control
- **Generic embedded** — UART serial interface for any microcontroller

### Real Sensors Supported
- **IMU (MPU-6050)** — Accelerometer, gyroscope
- **Barometer (BMP388)** — Altitude from pressure
- **Magnetometer (HMC5883L)** — Compass heading
- **GPS (NMEA protocol)** — Real coordinates
- **Battery monitoring** — Voltage and remaining capacity

### Example: Controlling Real Hardware

```python
from northwind.advanced import VehicleController

# Create controller for real Raspberry Pi
vehicle = VehicleController(platform='raspberry_pi', use_hardware=True)

# Connect to real hardware (reads actual sensors)
vehicle.connect()

# Arm motors and send real PWM signals
vehicle.arm()

# Real attitude control - sends actual signals to ESCs
vehicle.set_attitude(pitch=10, roll=-5, yaw=0, throttle=0.6)

# Real telemetry from sensors
location = vehicle.get_location()  # Real GPS
attitude = vehicle.get_attitude()   # Real IMU
battery = vehicle.get_battery_status()  # Real voltage

# Control actual motors
vehicle.set_attitude(pitch, roll, yaw, throttle)
```

### Example: Real Hardware with Arduino/Pico

```python
from northwind.advanced import VehicleController

# Connect to Arduino or Pico via serial
vehicle = VehicleController(use_hardware=True)
vehicle.connect('COM3', baud=115200)

vehicle.arm_and_takeoff(altitude=2.0)
# This sends REAL PWM values to motors!
```

## Features


Northwind provides two ways to interact with drone control systems:

### 1. **Simplified Drone Shortcut** (`from northwind import drone`)
Direct, function-based API for quick scripts and prototyping.
- Motor control: `drone.set_speed()`, `drone.ramp_speed()`, `drone.stop()`
- Mission control: `drone.initialize()`, `drone.calibrate()`, `drone.fly()`, `drone.land()`, `drone.home()`
- Navigation: `drone.set_destination()`, `drone.plan_route()`, `drone.update_position()`
- Obstacle avoidance: `drone.check_obstacle()`, `drone.avoid()`, `drone.recalculate_path()`
- Stability: `drone.correct_drift()`, `drone.adjust_altitude()`, `drone.hover()`
- Sensors: `drone.scan()`, `drone.detect_moving_obstacles()`, `drone.health_check()`
- AI decisions: `drone.decide()`, `drone.predict_move()`
- Logging: `drone.log_data()`, `drone.export()`, `drone.upload_cloud()`

### 2. **Full Module API** (Traditional import)
Modular architecture for complex applications.
- **Navigation** — Location and route math
- **Obstacle Handling** — Sensor-based obstacle detection and avoidance
- **Stability/Correction** — GPS drift, altitude adjustment, position hold
- **Mission Control** — Mission lifecycle, waypoints, validation
- **Motor Control** — PWM speed control for ESP32/Arduino/drone ESC
- **AI Decision Layer** — State-based action selection
- **Data Logging** — Telemetry recording and cloud export

### 3. **Advanced Flight Control** (`from northwind.advanced import VehicleController`)
High-level drone operations with safety systems.

**Connection & Setup:**
- `connect(address, wait_ready=True)` — Connect to drone via USB/radio/network
- `disconnect()` — Close connection

**Telemetry & State Monitoring:**
- `get_armed()`, `get_mode()`, `get_location()` — Read vehicle state
- `get_attitude()`, `get_velocity()` — Monitor dynamics
- `get_battery_status()` — Battery voltage, current, remaining
- `get_system_status()` — Overall health

**Flight Control:**
- `arm()`, `disarm()` — Motor control
- `arm_and_takeoff(altitude)` — Takeoff to target altitude
- `simple_goto(lat, lon, alt)` — Fly to GPS location
- `set_velocity_body(vx, vy, vz)` — Body-frame velocity control
- `set_attitude(pitch, roll, yaw, throttle)` — Low-level angle control
- `land()` — Auto-land at current location

**Mission Planning:**
- `upload_mission(waypoints)` — Load waypoint list
- `start_mission()`, `pause_mission()`, `resume_mission()` — Mission control
- `set_region_of_interest(location)` — Point camera at target
- `command_long(cmd_id, params)` — Custom MAVLink commands

**Safety & Failsafes:**
- `return_to_launch()` — RTL mode (auto-return and land)
- `set_battery_failsafe(threshold, action)` — Low-battery protection
- `check_battery_failsafe()` — Trigger battery failsafe logic
- `enable_geofence(radius)` — Circular boundary protection
- `check_geofence(location)` — Verify location is within bounds
- `emergency_stop()` — Immediate disarm (emergency only)
- `get_failsafe_status()` — Review safety configuration


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

### Simplified Shortcut API (Recommended for scripts)

```python
from northwind import drone

# Initialize and configure
drone.initialize()
drone.calibrate()
drone.set_mode('autonomous')

# Configure motor hardware
drone.config_device('esp32')

# Execute a flight mission
drone.fly([(0.0, 0.0), (10.5, 20.3), (15.2, 25.1)])

# If needed, adjust speed during flight
drone.set_speed(75)  # 75% throttle
drone.ramp_speed(90, step=5, delay=0.1)  # Smooth ramp to 90%

# Return home and land
drone.home()
drone.land()

# Check system health
status = drone.health_check()
print(status)

# Log and export flight data
drone.log_telemetry()
drone.export()
```

### Full Module Access (Advanced)

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

# Decision helpers
action = northwind.choose_action('normal')
next_move = northwind.predict_next_move()

# Log flight data
northwind.log_flight_data()
northwind.export_data()
```

### Advanced Flight Control (Waypoint missions, failsafes, geofence)

```python
from northwind.advanced import VehicleController

# Create vehicle controller
vehicle = VehicleController()

# Connect to drone
vehicle.connect('COM3', wait_ready=True)

# Arm and takeoff
vehicle.arm_and_takeoff(target_altitude=20)

# Upload waypoint mission
waypoints = [
    (37.7749, -122.4194, 20),
    (37.7750, -122.4195, 25),
    (37.7751, -122.4196, 30),
]
vehicle.upload_mission(waypoints)

# Configure safety
vehicle.set_battery_failsafe(threshold=20, action='RTL')
vehicle.enable_geofence(radius=1000)

# Start autonomous mission
vehicle.start_mission()

# Monitor telemetry
while vehicle.get_armed():
    location = vehicle.get_location()
    battery = vehicle.get_battery_status()
    print(f"Alt: {location['altitude_relative']:.1f}m, Battery: {battery['remaining']:.0f}%")
    
    # Check failsafes
    vehicle.check_battery_failsafe()

# Land
vehicle.land()
vehicle.disconnect()
```

## Motor Speed Control

Northwind 1.2.2 provides PWM-based motor speed control for ESP32, Arduino, and drone hardware platforms.

### Supported Devices
- `esp32` — ESP32 PWM driver (0-255 range, 1000 Hz)
- `arduino` — Arduino PWM driver (0-255 range, 490 Hz)
- `drone` — Generic drone ESC (1000-2000 µs range, 400 Hz)

### Using the Simplified Drone API
```python
from northwind import drone

# Select hardware device
drone.config_device('esp32')

# Set speed directly
drone.set_speed(50)  # 50% throttle

# Ramp speed smoothly
drone.ramp_speed(100, step=10, delay=0.05)

# Check motor status
status = drone.motor_status()
print(f"Current PWM: {status['current_pwm']}")

# Stop motor
drone.stop()
```

### Using pwm values directly
```python
from northwind import motors

motors.set_hardware_device('esp32')
motors.set_motor_speed_pwm(128)  # Mid-range for ESP32
```


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