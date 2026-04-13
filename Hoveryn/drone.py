"""
Simplified Drone Shortcut Module for Hoveryn

Provides direct access to drone control functions without the module prefix.
Use this for quick scripts and demonstrations.

Example:
    from Hoveryn.drone import fly, set_speed, land
    
    # Set hardware and speed
    set_speed(75)  # 75% throttle
    
    # Execute mission
    fly([(0, 0), (10, 10)])
    
    # Land
    land()
"""

from . import motors
from . import mission_control
from . import navigation
from . import stability
from . import obstacle_handling
from . import ai_decision
from . import data_logging


# ============================================================================
# MOTOR CONTROL - PWM Speed Management
# ============================================================================

def config_device(device_type: str):
    """Configure motor controller for hardware device (esp32, arduino, or drone).
    
    Args:
        device_type: 'esp32', 'arduino', or 'drone'
    
    Example:
        config_device('esp32')
    """
    return motors.set_hardware_device(device_type)


def set_speed(percent: float):
    """Set motor speed as percentage (0-100%).
    
    Args:
        percent: Motor speed percentage
    
    Example:
        set_speed(75)  # 75% throttle
    """
    return motors.set_motor_speed(percent)


def set_speed_pwm(pwm: float):
    """Set motor speed directly using PWM value.
    
    Args:
        pwm: PWM value (range depends on device)
    
    Example:
        set_speed_pwm(128)  # For ESP32 (0-255 range)
    """
    return motors.set_motor_speed_pwm(pwm)


def ramp_speed(target_percent: float, step: float = 5.0, delay: float = 0.05):
    """Smoothly ramp motor speed to target percent.
    
    Args:
        target_percent: Target speed percentage
        step: Speed increment per step
        delay: Delay between steps in seconds
    
    Example:
        ramp_speed(90, step=10, delay=0.1)  # Ramp to 90% in 10% steps
    """
    return motors.ramp_motor_speed(target_percent, step=step, delay=delay)


def motor_status():
    """Get current motor controller status.
    
    Returns:
        dict: Motor status including PWM, speed percent, and device profile
    
    Example:
        status = motor_status()
        print(status['current_pwm'])
    """
    return motors.get_motor_status()


def stop():
    """Stop motor immediately.
    
    Example:
        stop()
    """
    return motors.stop_motor()


# ============================================================================
# NAVIGATION - Flight Path Control
# ============================================================================

def set_destination(lat: float, lon: float):
    """Set navigation destination coordinates.
    
    Args:
        lat: Destination latitude
        lon: Destination longitude
    
    Example:
        set_destination(37.7749, -122.4194)  # San Francisco
    """
    return navigation.set_destination(lat, lon)


def plan_route(start: tuple, end: tuple):
    """Calculate flight route between two coordinates.
    
    Args:
        start: (lat, lon) starting position tuple
        end: (lat, lon) ending position tuple
    
    Returns:
        list: Series of waypoints
    
    Example:
        route = plan_route((0.0, 0.0), (37.7749, -122.4194))
    """
    return navigation.calculate_route(start, end)


def update_position():
    """Update current drone position from sensors.
    
    Returns:
        tuple: Current (lat, lon) position
    
    Example:
        position = update_position()
    """
    return navigation.update_position()


# ============================================================================
# OBSTACLE DETECTION & AVOIDANCE
# ============================================================================

def check_obstacle(sensor_data: dict):
    """Detect obstacles at current location using sensor data.
    
    Args:
        sensor_data: Dictionary with distance and sensor readings
    
    Returns:
        bool: True if obstacle detected
    
    Example:
        if check_obstacle({'distance': 2.0}):
            print("Obstacle ahead!")
    """
    return obstacle_handling.detect_obstacle(sensor_data)


def avoid(direction: str):
    """Execute obstacle avoidance maneuver.
    
    Args:
        direction: 'left', 'right', 'up', or 'down'
    
    Example:
        avoid('left')
    """
    return obstacle_handling.avoid_obstacle(direction)


def recalculate_path():
    """Recalculate flight path to avoid obstacles.
    
    Returns:
        list: New waypoints
    
    Example:
        new_path = recalculate_path()
    """
    return obstacle_handling.recalculate_path()


# ============================================================================
# STABILITY & CORRECTION
# ============================================================================

def correct_drift(gps_error: tuple):
    """Correct GPS positioning drift.
    
    Args:
        gps_error: (lat_error, lon_error) tuple
    
    Example:
        correct_drift((0.001, -0.002))
    """
    return stability.correct_drift(gps_error)


def adjust_altitude(wind_data: dict):
    """Adjust altitude based on wind conditions.
    
    Args:
        wind_data: Dictionary with 'speed', 'direction', etc.
    
    Example:
        adjust_altitude({'speed': 20, 'direction': 'N'})
    """
    return stability.adjust_altitude(wind_data)


def hover():
    """Engage hover/position hold mode.
    
    Example:
        hover()
    """
    return stability.hold_position()


# ============================================================================
# MISSION CONTROL - Flight Execution
# ============================================================================

def initialize():
    """Boot and reset all drone systems.
    
    Example:
        initialize()
    """
    return mission_control.initialize_system()


def calibrate():
    """Calibrate GPS, IMU, and camera sensors.
    
    Example:
        calibrate()
    """
    return mission_control.calibrate_sensors()


def set_mode(mode: str):
    """Switch flight mode.
    
    Args:
        mode: 'manual', 'assist', or 'autonomous'
    
    Example:
        set_mode('autonomous')
    """
    return mission_control.set_flight_mode(mode)


def define_mission(waypoints):
    """Define flight mission waypoints.
    
    Args:
        waypoints: List of (lat, lon) tuples or path to JSON file
    
    Example:
        define_mission([(0, 0), (10, 10), (20, 20)])
    """
    return mission_control.define_mission(waypoints)


def validate():
    """Validate mission safety and feasibility.
    
    Returns:
        bool: True if mission is safe
    
    Example:
        if validate():
            print("Mission ready!")
    """
    return mission_control.validate_mission()


def estimate_battery():
    """Estimate battery usage for current mission.
    
    Returns:
        float: Battery percentage needed
    
    Example:
        battery_needed = estimate_battery()
    """
    return mission_control.estimate_battery_usage()


def optimize():
    """Optimize flight route for efficiency.
    
    Returns:
        list: Optimized waypoints
    
    Example:
        optimized = optimize()
    """
    return mission_control.optimize_route()


def scan():
    """Gather real-time environment sensor data.
    
    Returns:
        dict: Sensor data including distance, GPS signal, wind, etc.
    
    Example:
        environment = scan()
    """
    return mission_control.scan_environment()


def detect_moving_obstacles():
    """Identify moving objects from sensor scan.
    
    Returns:
        list: Detected obstacles with distance/type
    
    Example:
        obstacles = detect_moving_obstacles()
    """
    return mission_control.detect_dynamic_obstacles()


def update_world_map():
    """Update internal map of surroundings.
    
    Returns:
        dict: Updated world model
    
    Example:
        world = update_world_map()
    """
    return mission_control.update_world_model()


def fly(waypoints: list):
    """Execute flight mission with waypoints.
    
    Full mission lifecycle: initialize → calibrate → define → validate → optimize → simulate → start
    
    Args:
        waypoints: List of (lat, lon) coordinate tuples
    
    Returns:
        list: Executed flight route
    
    Example:
        route = fly([(0, 0), (10, 10), (20, 20)])
    """
    drone_obj = mission_control.Drone()
    return drone_obj.fly(waypoints)


def start():
    """Start autonomous mission execution.
    
    Example:
        start()
    """
    return mission_control.start_mission()


def pause():
    """Pause current mission.
    
    Example:
        pause()
    """
    return mission_control.pause_mission()


def land():
    """Land drone safely at current location.
    
    Example:
        land()
    """
    return mission_control.auto_land()


def home():
    """Return to home/base position.
    
    Example:
        home()
    """
    return mission_control.return_to_base()


def emergency():
    """Trigger emergency protocol (hover safe mode).
    
    Example:
        emergency()
    """
    return mission_control.emergency_protocol()


def simulate():
    """Run mission in simulation before execution.
    
    Example:
        simulate()
    """
    return mission_control.simulate_mission()


def health_check():
    """Check system health and component status.
    
    Returns:
        dict: Health status and any issues
    
    Example:
        status = health_check()
    """
    return mission_control.health_check()


def log_telemetry():
    """Record flight telemetry and sensor data.
    
    Example:
        log_telemetry()
    """
    return mission_control.log_telemetry()


def sync_cloud():
    """Upload logs and status to cloud.
    
    Example:
        sync_cloud()
    """
    return mission_control.sync_cloud()


def download_updates():
    """Fetch AI model and config updates.
    
    Example:
        download_updates()
    """
    return mission_control.download_updates()


# ============================================================================
# AI DECISION ENGINE
# ============================================================================

def decide(state: str):
    """Choose optimal action based on drone state.
    
    Args:
        state: Drone state like 'normal', 'low_battery', 'obstacle_detected'
    
    Returns:
        str: Recommended action
    
    Example:
        action = decide('obstacle_detected')
    """
    return ai_decision.choose_action(state)


def predict_move():
    """Predict next optimal move using AI.
    
    Returns:
        str: Predicted next move
    
    Example:
        next_action = predict_move()
    """
    return ai_decision.predict_next_move()


# ============================================================================
# DATA LOGGING & EXPORT
# ============================================================================

def log_data():
    """Log current flight data.
    
    Example:
        log_data()
    """
    return data_logging.log_flight_data()


def export():
    """Export logged data to JSON file.
    
    Example:
        export()
    """
    return data_logging.export_data()


def upload_cloud():
    """Upload data to cloud storage.
    
    Example:
        upload_cloud()
    """
    return data_logging.send_to_cloud()


__all__ = [
    # Motor Control
    'config_device',
    'set_speed',
    'set_speed_pwm',
    'ramp_speed',
    'motor_status',
    'stop',
    # Navigation
    'set_destination',
    'plan_route',
    'update_position',
    # Obstacle Handling
    'check_obstacle',
    'avoid',
    'recalculate_path',
    # Stability
    'correct_drift',
    'adjust_altitude',
    'hover',
    # Mission Control
    'initialize',
    'calibrate',
    'set_mode',
    'define_mission',
    'validate',
    'estimate_battery',
    'optimize',
    'scan',
    'detect_moving_obstacles',
    'update_world_map',
    'fly',
    'start',
    'pause',
    'land',
    'home',
    'emergency',
    'simulate',
    'health_check',
    'log_telemetry',
    'sync_cloud',
    'download_updates',
    # AI Decision
    'decide',
    'predict_move',
    # Data Logging
    'log_data',
    'export',
    'upload_cloud',
]
