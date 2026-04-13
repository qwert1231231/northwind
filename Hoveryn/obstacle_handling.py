"""
Obstacle handling module for Hoveryn drone library.
Manages obstacle detection and avoidance with sensor-driven hardware input.
"""

from typing import Optional

from .flight_control import FlightControlSystem
from .hal import FlightControllerHAL, SimulatedHAL


class ObstacleHandler:
    def __init__(self, hal: Optional[FlightControllerHAL] = None, flight_control: Optional[FlightControlSystem] = None):
        self.hal = hal or SimulatedHAL()
        self.flight_control = flight_control
        self.obstacles_detected = []

    def scan_for_obstacle(self, threshold: float = 2.0) -> bool:
        distance = self.hal.read_distance_sensor()
        if distance is None:
            print("No distance sensor available for obstacle detection")
            return False
        if distance > 0 and distance < threshold:
            self.obstacles_detected.append({'distance': distance})
            print(f"Obstacle detected at {distance:.2f}m")
            return True
        print(f"No obstacle detected, distance={distance:.2f}m")
        return False

    def avoid_obstacle(self) -> bool:
        if self.flight_control is None:
            raise RuntimeError("Flight control system is required for avoidance maneuvers")

        print("Executing obstacle avoidance maneuver")
        self.flight_control.set_motor_mixes(-50, 0, 0, self.flight_control.base_throttle)
        self.flight_control.set_motor_mixes(0, -50, 0, self.flight_control.base_throttle)
        print("Avoidance maneuver issued")
        return True

    def reroute_path(self):
        print("Rerouting around detected obstacle")
        return self.obstacles_detected.copy()


_handler = ObstacleHandler()

def scan_for_obstacle(threshold: float = 2.0) -> bool:
    return _handler.scan_for_obstacle(threshold=threshold)


def detect_obstacle(sensor_data):
    distance = sensor_data.get('distance', None)
    if distance is None:
        return False
    return distance > 0 and distance < 2.0


def avoid_obstacle(direction=None):
    if direction is not None:
        print(f"Avoiding obstacle by moving {direction}")
    return _handler.avoid_obstacle()


def recalculate_path():
    return _handler.reroute_path()


def execute_avoidance() -> bool:
    return _handler.avoid_obstacle()


def reroute_path():
    return _handler.reroute_path()