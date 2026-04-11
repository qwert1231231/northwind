# Northwind Drone Navigation Library
# A comprehensive library for drone navigation, obstacle avoidance, stability control, mission management, AI decision making, and data logging.

__version__ = "1.1.2"

from . import navigation
from . import obstacle_handling
from . import stability
from . import mission_control
from . import ai_decision
from . import data_logging
from . import motors

# Import functions to package level for convenience
from .navigation import set_destination, calculate_route, update_position
from .obstacle_handling import detect_obstacle, avoid_obstacle, recalculate_path
from .stability import correct_drift, adjust_altitude, hold_position
from .mission_control import (
    Drone,
    quick_mission,
    quick_launch,
    land,
    home,
    initialize_system,
    calibrate_sensors,
    set_flight_mode,
    define_mission,
    validate_mission,
    estimate_battery_usage,
    optimize_route,
    scan_environment,
    detect_dynamic_obstacles,
    update_world_model,
    decision_engine,
    emergency_protocol,
    auto_land,
    return_to_base,
    hover_stable,
    log_telemetry,
    sync_cloud,
    download_updates,
    simulate_mission,
    health_check,
    start_mission,
    pause_mission,
    return_home,
)
from .ai_decision import choose_action, predict_next_move
from .data_logging import log_flight_data, export_data, send_to_cloud
from .motors import (
    MotorController,
    set_hardware_device,
    set_motor_speed,
    set_motor_speed_pwm,
    ramp_motor_speed,
    stop_motor,
    get_motor_status,
)

__all__ = [
    "navigation",
    "obstacle_handling", 
    "stability",
    "mission_control",
    "ai_decision",
    "data_logging",
    "motors",
    "set_destination",
    "calculate_route", 
    "update_position",
    "detect_obstacle",
    "avoid_obstacle",
    "recalculate_path",
    "correct_drift",
    "adjust_altitude",
    "hold_position",
    "Drone",
    "quick_mission",
    "quick_launch",
    "land",
    "home",
    "initialize_system",
    "calibrate_sensors",
    "set_flight_mode",
    "define_mission",
    "validate_mission",
    "estimate_battery_usage",
    "optimize_route",
    "scan_environment",
    "detect_dynamic_obstacles",
    "update_world_model",
    "decision_engine",
    "emergency_protocol",
    "auto_land",
    "return_to_base",
    "hover_stable",
    "log_telemetry",
    "sync_cloud",
    "download_updates",
    "simulate_mission",
    "health_check",
    "start_mission",
    "pause_mission",
    "return_home",
    "choose_action",
    "predict_next_move",
    "log_flight_data",
    "export_data",
    "send_to_cloud",
    "MotorController",
    "set_hardware_device",
    "set_motor_speed",
    "set_motor_speed_pwm",
    "ramp_motor_speed",
    "stop_motor",
    "get_motor_status",
]