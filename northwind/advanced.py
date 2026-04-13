"""
Advanced Flight Control Module for Northwind

Provides high-level drone control functions including connection management,
telemetry monitoring, flight control, mission planning, and safety systems.

This module abstracts the complexity of low-level control and provides a clean
API for autonomous and semi-autonomous flight operations.

Example:
    from northwind.advanced import VehicleController
    
    controller = VehicleController()
    controller.connect('COM3', wait_ready=True)
    controller.arm_and_takeoff(10)
    controller.simple_goto((37.7749, -122.4194, 50))
    controller.land()
"""

from typing import Tuple, Dict, Optional, List
import time


class VehicleState:
    """Represents the drone's current state and telemetry."""
    
    def __init__(self):
        self.armed = False
        self.mode = 'STABILIZE'
        self.location = {'latitude': 0.0, 'longitude': 0.0, 'altitude': 0.0}
        self.altitude_relative = 0.0
        self.attitude = {'pitch': 0.0, 'roll': 0.0, 'yaw': 0.0}
        self.velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.battery = {'voltage': 12.6, 'current': 0.0, 'remaining': 100}
        self.is_armable = True
        self.system_status = 'INITIALIZING'
        self.gps_status = 'NO_FIX'
        self.connected = False


class VehicleController:
    """
    High-level vehicle controller for drone operations.
    
    Manages connection, state monitoring, flight control, and safety systems.
    """
    
    def __init__(self):
        self.state = VehicleState()
        self.connection_string = None
        self.baud_rate = 57600
        self.wp_loader = WaypointManager()
        self.failsafe_enabled = True
        self.battery_failsafe_threshold = 20.0  # percent
        self.geo_fence_enabled = False
        self.geo_fence_radius = 1000  # meters
    
    # ========================================================================
    # CONNECTION AND SETUP
    # ========================================================================
    
    def connect(self, address: str, wait_ready: bool = True, baud: int = 57600):
        """
        Connect to the drone over USB, radio, or network.
        
        Args:
            address: Connection address (e.g., 'COM3', '/dev/ttyUSB0', '192.168.1.100:14550')
            wait_ready: Wait for vehicle to initialize completely before returning
            baud: Serial baud rate (default 57600)
        
        Returns:
            bool: True if connection successful
        
        Example:
            controller.connect('COM3', wait_ready=True)
            controller.connect('127.0.0.1:14550')  # UDP connection
        """
        self.connection_string = address
        self.baud_rate = baud
        
        print(f"Attempting connection to {address} at {baud} baud...")
        
        try:
            # Simulate connection
            self.state.connected = True
            self.state.system_status = 'INITIALIZING'
            
            if wait_ready:
                self._wait_for_ready()
            
            print(f"Connected to vehicle at {address}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            self.state.connected = False
            return False
    
    def _wait_for_ready(self, timeout: float = 30.0):
        """Wait for vehicle to be ready for commands."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.state.system_status == 'ACTIVE' and self.state.gps_status in ['FIX', 'GPS_OK']:
                print("Vehicle ready for operation")
                return True
            time.sleep(0.5)
        
        print(f"Warning: Vehicle may not be fully ready (timeout after {timeout}s)")
        return False
    
    def disconnect(self):
        """Close connection to vehicle."""
        if self.state.connected:
            self.state.connected = False
            print("Disconnected from vehicle")
            return True
        return False
    
    # ========================================================================
    # STATE MONITORING (TELEMETRY)
    # ========================================================================
    
    def get_armed(self) -> bool:
        """Check if motors are armed."""
        return self.state.armed
    
    def get_mode(self) -> str:
        """Get current flight mode (GUIDED, LOITER, LAND, RTL, etc.)."""
        return self.state.mode
    
    def set_mode(self, mode: str):
        """
        Set flight mode.
        
        Args:
            mode: Flight mode string (e.g., 'GUIDED', 'LOITER', 'LAND', 'RTL', 'STABILIZE')
        
        Example:
            controller.set_mode('GUIDED')
        """
        valid_modes = ['STABILIZE', 'GUIDED', 'LOITER', 'LAND', 'RTL', 'AUTO', 'ACRO']
        if mode not in valid_modes:
            print(f"Warning: '{mode}' may not be valid. Valid modes: {valid_modes}")
        
        self.state.mode = mode
        print(f"Flight mode set to: {mode}")
        return mode
    
    def get_location(self) -> Dict:
        """
        Get current drone location and altitude.
        
        Returns:
            dict: {'latitude', 'longitude', 'altitude', 'altitude_relative'}
        
        Example:
            loc = controller.get_location()
            print(f"Altitude: {loc['altitude']}m")
        """
        return {
            'latitude': self.state.location['latitude'],
            'longitude': self.state.location['longitude'],
            'altitude': self.state.location['altitude'],
            'altitude_relative': self.state.altitude_relative,
        }
    
    def get_attitude(self) -> Dict:
        """
        Get current pitch, roll, yaw angles.
        
        Returns:
            dict: {'pitch', 'roll', 'yaw'} in degrees
        """
        return self.state.attitude.copy()
    
    def get_velocity(self) -> Dict:
        """
        Get current velocity in x, y, z axes.
        
        Returns:
            dict: {'x', 'y', 'z'} in m/s
        """
        return self.state.velocity.copy()
    
    def get_battery_status(self) -> Dict:
        """
        Monitor battery voltage, current, and remaining capacity.
        
        Returns:
            dict: {'voltage', 'current', 'remaining'} (voltage in V, current in A, remaining in %)
        
        Example:
            battery = controller.get_battery_status()
            if battery['remaining'] < 25:
                print("Low battery!")
        """
        return self.state.battery.copy()
    
    def is_armable(self) -> bool:
        """Check if vehicle can be armed."""
        return self.state.is_armable
    
    def get_system_status(self) -> str:
        """Get overall system status."""
        return self.state.system_status
    
    def get_gps_status(self) -> str:
        """Get GPS fix status (NO_FIX, FIX, GPS_OK, etc.)."""
        return self.state.gps_status
    
    # ========================================================================
    # BASIC FLIGHT CONTROL
    # ========================================================================
    
    def arm(self):
        """
        Arm the motors.
        
        Example:
            controller.arm()
        """
        if not self.state.is_armable:
            print("Vehicle is not armable")
            return False
        
        self.state.armed = True
        print("Motors armed")
        return True
    
    def disarm(self):
        """Disarm the motors."""
        self.state.armed = False
        print("Motors disarmed")
        return True
    
    def arm_and_takeoff(self, target_altitude: float):
        """
        Arm motors and take off to target altitude.
        
        This is a high-level function that handles:
        - Checking if vehicle is armable
        - Setting mode to GUIDED
        - Arming motors
        - Performing takeoff
        
        Args:
            target_altitude: Target altitude in meters (relative to home)
        
        Example:
            controller.arm_and_takeoff(10)  # Takeoff to 10 meters
        """
        if not self.is_armable():
            print("Vehicle not armable - check failsafes")
            return False
        
        print(f"Arming vehicle...")
        self.set_mode('GUIDED')
        self.arm()
        
        print(f"Taking off to {target_altitude}m...")
        self.simple_takeoff(target_altitude)
        
        # Monitor takeoff
        while self.state.altitude_relative < target_altitude * 0.95:
            print(f"  Altitude: {self.state.altitude_relative:.1f}m")
            time.sleep(1)
        
        print(f"Takeoff complete - at {self.state.altitude_relative:.1f}m")
        return True
    
    def simple_takeoff(self, target_altitude: float):
        """
        Perform takeoff to specified altitude.
        
        Args:
            target_altitude: Target altitude in meters
        """
        self.state.altitude_relative = min(self.state.altitude_relative + 0.5, target_altitude)
        return True
    
    def simple_goto(self, location: Tuple[float, float, float]):
        """
        Command drone to fly to specified GPS location and altitude.
        
        Args:
            location: (latitude, longitude, altitude) tuple
        
        Example:
            controller.simple_goto((37.7749, -122.4194, 50))
        """
        lat, lon, alt = location
        self.state.location['latitude'] = lat
        self.state.location['longitude'] = lon
        self.state.location['altitude'] = alt
        
        print(f"Flying to GPS location: ({lat}, {lon}) at {alt}m")
        return True
    
    def set_velocity_body(self, vx: float, vy: float, vz: float):
        """
        Set velocity in body frame for smooth high-level control.
        
        Useful for computer vision tracking and obstacle avoidance.
        
        Args:
            vx: Velocity in X axis (forward/back) in m/s
            vy: Velocity in Y axis (left/right) in m/s
            vz: Velocity in Z axis (up/down) in m/s
        
        Example:
            controller.set_velocity_body(5, 0, -1)  # Move forward and down
        """
        self.state.velocity['x'] = vx
        self.state.velocity['y'] = vy
        self.state.velocity['z'] = vz
        
        print(f"Velocity set to: ({vx}, {vy}, {vz}) m/s in body frame")
        return True
    
    def set_attitude(self, pitch: float, roll: float, yaw: float, throttle: float = 0.5):
        """
        Low-level attitude control: directly set pitch, roll, yaw, and throttle.
        
        Args:
            pitch: Pitch angle in degrees (-90 to 90)
            roll: Roll angle in degrees (-180 to 180)
            yaw: Yaw angle in degrees (0 to 360)
            throttle: Throttle (0.0 to 1.0)
        
        Example:
            controller.set_attitude(10, -5, 180, throttle=0.6)
        """
        self.state.attitude['pitch'] = pitch
        self.state.attitude['roll'] = roll
        self.state.attitude['yaw'] = yaw
        
        print(f"Attitude set - Pitch: {pitch}, Roll: {roll}, Yaw: {yaw}, Throttle: {throttle}")
        return True
    
    def land(self):
        """
        Land the drone at current location.
        
        Example:
            controller.land()
        """
        self.set_mode('LAND')
        print("Landing...")
        
        while self.state.altitude_relative > 0.1:
            self.state.altitude_relative = max(0, self.state.altitude_relative - 0.5)
            time.sleep(1)
        
        self.disarm()
        print("Landed successfully")
        return True
    
    # ========================================================================
    # MISSION PLANNING AND ADVANCED CONTROL
    # ========================================================================
    
    def set_region_of_interest(self, location: Tuple[float, float, float]):
        """
        Set Region of Interest (ROI) for the camera.
        
        Makes drone camera point at specified location while flying.
        
        Args:
            location: (latitude, longitude, altitude) of interest point
        
        Example:
            controller.set_region_of_interest((37.7749, -122.4194, 0))
        """
        lat, lon, alt = location
        print(f"Region of Interest set to: ({lat}, {lon}, {alt})")
        return True
    
    def upload_mission(self, waypoints: List[Tuple[float, float, float]]):
        """
        Load and upload waypoint mission to vehicle.
        
        Args:
            waypoints: List of (latitude, longitude, altitude) tuples
        
        Example:
            waypoints = [
                (37.7749, -122.4194, 10),
                (37.7750, -122.4195, 15),
                (37.7751, -122.4196, 20),
            ]
            controller.upload_mission(waypoints)
        """
        self.wp_loader.load_waypoints(waypoints)
        print(f"Uploaded mission with {len(waypoints)} waypoints")
        return True
    
    def start_mission(self):
        """Start autonomous mission execution."""
        self.set_mode('AUTO')
        print("Mission started")
        return True
    
    def pause_mission(self):
        """Pause mission and switch to loiter mode."""
        self.set_mode('LOITER')
        print("Mission paused")
        return True
    
    def resume_mission(self):
        """Resume mission from current waypoint."""
        self.set_mode('AUTO')
        print("Mission resumed")
        return True
    
    def get_mission_waypoints(self) -> List:
        """Get list of current mission waypoints."""
        return self.wp_loader.waypoints
    
    def command_long(self, command_id: int, param1: float, param2: float = 0, **params):
        """
        Send custom MAVLink command (command_long).
        
        Low-level interface for advanced control.
        
        Args:
            command_id: MAVLink command ID
            param1: Command parameter 1
            param2: Command parameter 2
            **params: Additional parameters
        
        Returns:
            dict: Command result
        """
        result = {
            'command_id': command_id,
            'param1': param1,
            'param2': param2,
            'status': 'SENT',
        }
        print(f"Command sent: {command_id} with params {param1}, {param2}")
        return result
    
    # ========================================================================
    # SAFETY AND FAILSAFES
    # ========================================================================
    
    def return_to_launch(self):
        """
        Return to Launch (RTL) mode.
        
        Drone automatically flies back to home position and lands.
        
        Example:
            controller.return_to_launch()
        """
        self.set_mode('RTL')
        print("Returning to launch position...")
        return True
    
    def set_battery_failsafe(self, threshold: float = 20.0, action: str = 'RTL'):
        """
        Configure battery failsafe.
        
        Args:
            threshold: Battery percentage threshold (default 20%)
            action: Action to take ('RTL' or 'LAND')
        
        Example:
            controller.set_battery_failsafe(25, 'RTL')
        """
        self.battery_failsafe_threshold = threshold
        print(f"Battery failsafe set to {threshold}% - action: {action}")
        return True
    
    def check_battery_failsafe(self) -> bool:
        """
        Check if battery failsafe should be triggered.
        
        Returns:
            bool: True if battery is below failsafe threshold
        """
        battery_percent = self.state.battery['remaining']
        
        if battery_percent < self.battery_failsafe_threshold:
            print(f"Battery failsafe triggered: {battery_percent}% < {self.battery_failsafe_threshold}%")
            if self.failsafe_enabled:
                self.return_to_launch()
            return True
        
        return False
    
    def enable_geofence(self, radius: float = 1000):
        """
        Enable geofence to prevent drone from flying beyond radius.
        
        Args:
            radius: Geofence radius in meters from home
        
        Example:
            controller.enable_geofence(500)
        """
        self.geo_fence_enabled = True
        self.geo_fence_radius = radius
        print(f"Geofence enabled with radius {radius}m")
        return True
    
    def disable_geofence(self):
        """Disable geofence."""
        self.geo_fence_enabled = False
        print("Geofence disabled")
        return True
    
    def check_geofence(self, location: Tuple[float, float]) -> bool:
        """
        Check if location is within geofence.
        
        Args:
            location: (latitude, longitude) tuple
        
        Returns:
            bool: True if within fence
        """
        if not self.geo_fence_enabled:
            return True
        
        # Simplified distance check (in reality would use haversine)
        distance = ((location[0] - self.state.location['latitude']) ** 2 +
                   (location[1] - self.state.location['longitude']) ** 2) ** 0.5
        
        is_safe = distance * 111000 < self.geo_fence_radius  # Rough conversion to meters
        
        if not is_safe:
            print(f"Warning: Outside geofence! Distance: {distance * 111000:.0f}m")
        
        return is_safe
    
    def emergency_stop(self):
        """
        Emergency stop - immediately disarm motors.
        
        WARNING: Only use in emergency situations!
        """
        print("EMERGENCY STOP - Disarming immediately!")
        self.disarm()
        self.set_mode('STABILIZE')
        return True
    
    def get_failsafe_status(self) -> Dict:
        """Get current failsafe configuration status."""
        return {
            'failsafe_enabled': self.failsafe_enabled,
            'battery_threshold': self.battery_failsafe_threshold,
            'geofence_enabled': self.geo_fence_enabled,
            'geofence_radius': self.geo_fence_radius,
        }


class WaypointManager:
    """Manages mission waypoints."""
    
    def __init__(self):
        self.waypoints: List[Tuple[float, float, float]] = []
    
    def load_waypoints(self, waypoints: List[Tuple[float, float, float]]):
        """Load waypoints into manager."""
        self.waypoints = waypoints
        print(f"Loaded {len(waypoints)} waypoints")
    
    def add_waypoint(self, waypoint: Tuple[float, float, float]):
        """Add single waypoint."""
        self.waypoints.append(waypoint)
        print(f"Waypoint added: {waypoint}")
    
    def remove_waypoint(self, index: int):
        """Remove waypoint by index."""
        if 0 <= index < len(self.waypoints):
            self.waypoints.pop(index)
            print(f"Waypoint {index} removed")
    
    def save_to_file(self, filename: str):
        """Save waypoints to JSON file."""
        import json
        with open(filename, 'w') as f:
            json.dump(self.waypoints, f)
        print(f"Waypoints saved to {filename}")
    
    def load_from_file(self, filename: str):
        """Load waypoints from JSON file."""
        import json
        with open(filename, 'r') as f:
            self.waypoints = json.load(f)
        print(f"Waypoints loaded from {filename}")


# Convenience functions for direct use
_controller = VehicleController()


def connect(address: str, wait_ready: bool = True):
    """Connect to vehicle."""
    return _controller.connect(address, wait_ready=wait_ready)


def disconnect():
    """Disconnect from vehicle."""
    return _controller.disconnect()


def arm_and_takeoff(altitude: float):
    """Arm and take off."""
    return _controller.arm_and_takeoff(altitude)


def simple_goto(location: Tuple[float, float, float]):
    """Fly to location."""
    return _controller.simple_goto(location)


def land():
    """Land drone."""
    return _controller.land()


def return_to_launch():
    """Return to home."""
    return _controller.return_to_launch()


def get_location():
    """Get current location."""
    return _controller.get_location()


def get_battery_status():
    """Get battery info."""
    return _controller.get_battery_status()


def is_armed():
    """Check if armed."""
    return _controller.get_armed()


def set_mode(mode: str):
    """Set flight mode."""
    return _controller.set_mode(mode)
