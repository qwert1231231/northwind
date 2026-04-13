"""
Navigation module for Northwind drone library.
Handles destination setting, route planning, and hardware-driven navigation.
"""

import math
from typing import Dict, List, Optional, Tuple

from .hal import FlightControllerHAL, SimulatedHAL
from .sensor_fusion import SensorFusion


class NavigationSystem:
    def __init__(self, hal: Optional[FlightControllerHAL] = None, fusion: Optional[SensorFusion] = None):
        self.hal = hal or SimulatedHAL()
        self.fusion = fusion or SensorFusion()
        self.destination: Optional[Tuple[float, float]] = None
        self.current_position = (0.0, 0.0)
        self.altitude = 0.0
        self.waypoints: List[Tuple[float, float]] = []

    def set_destination(self, lat: float, lon: float) -> Tuple[float, float]:
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            raise TypeError('Latitude and longitude must be numeric values')
        self.destination = (lat, lon)
        print(f"Destination set to: {lat}, {lon}")
        return self.destination

    def plan_flight_path(self, start: Tuple[float, float], end: Tuple[float, float], steps: int = 5) -> List[Tuple[float, float]]:
        if not (isinstance(start, tuple) and isinstance(end, tuple)):
            raise TypeError('Start and end must be coordinate tuples')
        if steps < 2:
            raise ValueError('Steps must be at least 2')

        self.waypoints = [start]
        for i in range(1, steps):
            t = i / steps
            waypoint = (
                start[0] + (end[0] - start[0]) * t,
                start[1] + (end[1] - start[1]) * t,
            )
            self.waypoints.append(waypoint)
        self.waypoints.append(end)

        print(f"Planned flight path with {len(self.waypoints)} waypoints")
        return self.waypoints

    def refresh_position(self, dt: float = 0.02) -> Dict[str, float]:
        gps_data = self.hal.read_gps()
        imu_data = self.hal.read_imu()
        state = self.fusion.estimate_position(gps_data, imu_data, dt)
        self.current_position = (state['latitude'], state['longitude'])
        self.altitude = state['altitude']
        print(f"Refreshed position to {self.current_position}, altitude={self.altitude:.2f}")
        return state

    def _bearing_distance(self, start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float]:
        lat_diff = end[0] - start[0]
        lon_diff = end[1] - start[1]
        heading = math.degrees(math.atan2(lon_diff, lat_diff)) % 360
        distance = math.hypot(lat_diff, lon_diff) * 111.0
        return heading, distance, math.hypot(lat_diff, lon_diff)

    def navigate_to(self, target_lat: float, target_lon: float, dt: float = 0.02) -> Dict[str, float]:
        current_state = self.refresh_position(dt)
        current = (current_state['latitude'], current_state['longitude'])
        heading, distance, _ = self._bearing_distance(current, (target_lat, target_lon))
        print(f"Navigation target-heading={heading:.1f}°, distance={distance:.2f}km")
        return {
            'heading': heading,
            'distance_km': distance,
            'current_position': current,
            'target_position': (target_lat, target_lon),
        }


_nav = NavigationSystem()


def set_destination(lat: float, lon: float) -> Tuple[float, float]:
    return _nav.set_destination(lat, lon)


def plan_flight_path(start: Tuple[float, float], end: Tuple[float, float], steps: int = 5) -> List[Tuple[float, float]]:
    return _nav.plan_flight_path(start, end, steps=steps)


def refresh_position() -> Dict[str, float]:
    return _nav.refresh_position()


# Compatibility aliases
set_target_coordinate = set_destination
calculate_route = plan_flight_path
update_position = refresh_position
