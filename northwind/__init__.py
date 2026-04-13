# Northwind Drone Navigation Library
# Lightweight helper code for drone-style navigation, obstacle handling, and stability experiments.

__version__ = "1.2.3"

from . import navigation
from . import obstacle_handling
from . import stability
from . import mission_control
from . import ai_decision
from . import data_logging
from . import motors
from . import drone
from . import advanced
from . import hal
from . import flight_control
from . import sensor_fusion

# Import functions to package level for convenience
from .navigation import set_destination, calculate_route, update_position
from .obstacle_handling import scan_for_obstacle, execute_avoidance, reroute_path
from .stability import correct_drift, hold_position
from .actions import adjust_altitude
from .mission_control import (
    Mission,
    Drone,
    quick_mission,
    quick_launch,
    land,
    home,
    initialize_system,
    calibrate_sensors,
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
    set_motor_speeds,
    calibrate_esc,
    ramp_motor_speed,
    stop_motor,
    get_motor_status,
)
from .hal import FlightControllerHAL, SimulatedHAL
from .flight_control import FlightControlSystem
from .sensor_fusion import SensorFusion
from .actions import (
    set_target_coordinate,
    plan_flight_path,
    refresh_position,
    scan_for_obstacle as action_scan_for_obstacle,
    execute_avoidance as action_execute_avoidance,
    reroute_path as action_reroute_path,
    correct_gps_drift,
    adjust_altitude as action_adjust_altitude,
    engage_hover_hold,
    configure_motor_profile,
    set_motor_pwm,
    set_motor_speed_percent,
    ramp_motor_speed as action_ramp_motor_speed,
    stop_motor as action_stop_motor,
    read_motor_status,
)

__all__ = [
    "navigation",
    "obstacle_handling", 
    "stability",
    "mission_control",
    "ai_decision",
    "data_logging",
    "motors",
    "drone",
    "advanced",
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
    "set_motor_speeds",
    "calibrate_esc",
    "FlightControllerHAL",
    "SimulatedHAL",
    "FlightControlSystem",
    "SensorFusion",
    "Mission",
    "set_target_coordinate",
    "plan_flight_path",
    "refresh_position",
    "scan_for_obstacle",
    "execute_avoidance",
    "reroute_path",
    "correct_gps_drift",
    "adjust_altitude",
    "engage_hover_hold",
    "configure_motor_profile",
    "set_motor_pwm",
    "set_motor_speed_percent",
    "read_motor_status",
]