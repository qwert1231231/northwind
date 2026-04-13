"""
Mission control module for Hoveryn drone library.
Manages mission execution, safety, and hardware-aware flight sequencing.
"""

import datetime
import json
import math
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from .ai_decision import choose_action
from .data_logging import DataLogger
from .flight_control import FlightControlSystem
from .hal import FlightControllerHAL, SimulatedHAL
from .motors import MotorController
from .navigation import NavigationSystem
from .obstacle_handling import ObstacleHandler
from .sensor_fusion import SensorFusion


class Mission:
    def __init__(self, hal: Optional[FlightControllerHAL] = None):
        self.hal = hal or SimulatedHAL()
        self.fusion = SensorFusion()
        self.motor_controller = MotorController()
        self.flight_control = FlightControlSystem(self.hal, self.motor_controller, self.fusion)
        self.navigation = NavigationSystem(self.hal, self.fusion)
        self.obstacle_handler = ObstacleHandler(self.hal, self.flight_control)
        self.waypoints: List[Tuple[float, float]] = []
        self.active = False
        self.paused = False
        self.home_position = (0.0, 0.0)
        self.logger = DataLogger()
        self.health_status = {
            'battery': 100,
            'gps': True,
            'imu': True,
            'motors': True,
        }

    def calibrate(self) -> bool:
        print("Calibrating sensors and preparing hardware")
        self.flight_control.arm()
        self.motor_controller.calibrate_esc()
        self.paused = False
        return True

    def load_waypoints(self, path: Union[str, List[Tuple[float, float]]]) -> List[Tuple[float, float]]:
        if isinstance(path, str):
            with open(path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
            self.waypoints = payload.get('waypoints', []) if isinstance(payload, dict) else payload
        elif isinstance(path, (list, tuple)):
            self.waypoints = list(path)
        else:
            raise TypeError('Mission path must be a JSON file path or list of waypoints')

        if not self.waypoints:
            raise ValueError('Mission plan cannot be empty')

        self.home_position = self.waypoints[0] if self.waypoints else self.home_position
        print(f"Loaded {len(self.waypoints)} waypoints")
        return self.waypoints

    def validate(self) -> bool:
        if not self.waypoints:
            print('No mission loaded')
            return False
        if not self.health_status['gps'] or not self.health_status['imu']:
            print('Sensor health is not sufficient for flight')
            return False
        if self.estimate_battery_usage() > self.health_status['battery']:
            print('Battery estimate too low for mission')
            return False
        print('Mission validated')
        return True

    def estimate_battery_usage(self) -> int:
        if not self.waypoints:
            return 0
        total_distance = 0.0
        for current, next_wp in zip(self.waypoints, self.waypoints[1:]):
            total_distance += math.hypot(next_wp[0] - current[0], next_wp[1] - current[1]) * 111.0
        estimate = min(100, int(total_distance * 3 + len(self.waypoints) * 1.0))
        print(f"Estimated battery usage: {estimate}%")
        return estimate

    def execute(self) -> bool:
        if not self.validate():
            return False

        print('Starting mission execution')
        self.active = True
        for waypoint in self.waypoints:
            if self.paused or not self.active:
                print('Mission paused or stopped')
                break

            nav_state = self.navigation.navigate_to(*waypoint)
            steps = 0
            max_steps = 10  # Prevent infinite loop in simulation
            while nav_state['distance_km'] > 0.01 and self.active and not self.paused and steps < max_steps:
                if self.obstacle_handler.scan_for_obstacle():
                    action = choose_action('obstacle_detected')
                    if action == 'avoid':
                        self.obstacle_handler.avoid_obstacle()
                        self.obstacle_handler.reroute_path()
                        break
                self.flight_control.navigate_to(*waypoint)
                self.logger.log_flight_data()
                time.sleep(0.05)
                nav_state = self.navigation.navigate_to(*waypoint)
                steps += 1

            print(f"Reached waypoint {waypoint}")

        self.active = False
        print('Mission complete')
        return True

    def pause(self) -> None:
        self.paused = True
        print('Mission paused')

    def resume(self) -> None:
        self.paused = False
        print('Mission resumed')

    def return_home(self) -> Tuple[float, float]:
        print('Returning to home position')
        self.navigation.set_destination(*self.home_position)
        return self.home_position

    def land(self) -> bool:
        print('Landing sequence engaged')
        self.flight_control.disarm()
        self.active = False
        return True

    def health_check(self) -> Dict[str, Any]:
        issues = []
        if self.health_status['battery'] < 20:
            issues.append('low_battery')
        if not self.health_status['gps']:
            issues.append('gps_error')
        if not self.health_status['imu']:
            issues.append('imu_error')
        if not self.health_status['motors']:
            issues.append('motor_error')
        status = {'issues': issues, 'status': 'ok' if not issues else 'warning'}
        print('Health check:', status)
        return status


class Drone:
    def __init__(self, mode: str = 'autonomous', hal: Optional[FlightControllerHAL] = None):
        self.mission = Mission(hal=hal)
        self.mode = mode

    def prepare(self) -> bool:
        return self.mission.calibrate()

    def fly(self, path: Union[str, List[Tuple[float, float]]]) -> bool:
        self.mission.load_waypoints(path)
        self.mission.validate()
        return self.mission.execute()

    def home(self) -> Tuple[float, float]:
        return self.mission.return_home()

    def land(self) -> bool:
        return self.mission.land()

    def pause(self) -> None:
        self.mission.pause()

    def resume(self) -> None:
        self.mission.resume()

    def status(self) -> Dict[str, Any]:
        return self.mission.health_check()


_controller = Mission()


def quick_mission(path: Union[str, List[Tuple[float, float]]]) -> bool:
    return Drone().fly(path)


def quick_launch(path: Union[str, List[Tuple[float, float]]]) -> bool:
    return quick_mission(path)


def land() -> bool:
    return _controller.land()


def home() -> Tuple[float, float]:
    return _controller.return_home()


def initialize_system() -> bool:
    return _controller.calibrate()


def calibrate_sensors() -> bool:
    return _controller.calibrate()


def set_flight_mode(mode: str) -> str:
    raise NotImplementedError('Flight mode selection is handled per Drone instance')


def define_mission(path: Union[str, List[Tuple[float, float]]]) -> List[Tuple[float, float]]:
    return _controller.load_waypoints(path)


def validate_mission() -> bool:
    return _controller.validate()


def estimate_battery_usage() -> int:
    return _controller.estimate_battery_usage()


def optimize_route() -> List[Tuple[float, float]]:
    print('Optimize route: current implementation uses direct waypoint load')
    return _controller.waypoints


def scan_environment() -> Dict[str, Any]:
    print('Environment scan is not available in mission-only mode')
    return {}


def detect_dynamic_obstacles() -> List[Dict[str, Any]]:
    print('Dynamic obstacle detection is available through ObstacleHandler')
    return []


def update_world_model() -> Dict[str, Any]:
    print('World model update is not available in mission-only convenience wrapper')
    return {}


def decision_engine(state: Optional[str] = None) -> str:
    if not state:
        state = 'normal'
    return choose_action(state)


def emergency_protocol() -> bool:
    print('Emergency protocol triggered')
    return _controller.land()


def auto_land() -> bool:
    return _controller.land()


def return_to_base() -> Tuple[float, float]:
    return _controller.return_home()


def hover_stable() -> bool:
    print('Hover stable not available in mission-only wrapper')
    return False


def log_telemetry() -> bool:
    _controller.logger.log_flight_data()
    return True


def sync_cloud() -> bool:
    print('Cloud sync not available in mission-only wrapper')
    return False


def download_updates() -> Dict[str, Any]:
    print('No update service configured')
    return {'status': 'none'}


def simulate_mission() -> bool:
    print('Mission simulation is not supported in the new controller')
    return False


def health_check() -> Dict[str, Any]:
    return _controller.health_check()


def start_mission() -> bool:
    print('Start mission not supported on global controller, use Drone.fly()')
    return False


def pause_mission() -> None:
    _controller.pause()


def return_home() -> Tuple[float, float]:
    return _controller.return_home()