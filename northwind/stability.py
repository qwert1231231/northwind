"""
Stability and correction module for Northwind drone library.
Implements PID attitude control and position holding behavior.
"""

from dataclasses import dataclass


@dataclass
class PIDState:
    kp: float
    ki: float
    kd: float
    integral: float = 0.0
    last_error: float = 0.0

    def update(self, error: float, dt: float) -> float:
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        self.last_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class StabilityController:
    def __init__(self):
        self.roll_pid = PIDState(kp=1.0, ki=0.01, kd=0.05)
        self.pitch_pid = PIDState(kp=1.0, ki=0.01, kd=0.05)
        self.yaw_pid = PIDState(kp=0.8, ki=0.005, kd=0.03)
        self.altitude_pid = PIDState(kp=1.2, ki=0.02, kd=0.06)
        self.position_hold_active = False

    def correct_drift(self, gps_error, dt: float = 0.02):
        lat_error, lon_error = gps_error
        roll_correction = self.roll_pid.update(lat_error, dt)
        pitch_correction = self.pitch_pid.update(lon_error, dt)
        print(f"Drift corrections: roll={roll_correction:.3f}, pitch={pitch_correction:.3f}")
        return {'roll': roll_correction, 'pitch': pitch_correction}

    def adjust_altitude(self, current_altitude: float, target_altitude: float, dt: float = 0.02):
        altitude_error = target_altitude - current_altitude
        throttle_adjustment = self.altitude_pid.update(altitude_error, dt)
        print(f"Altitude correction: {throttle_adjustment:.3f} for error {altitude_error:.3f}")
        return throttle_adjustment

    def hold_position(self):
        self.position_hold_active = True
        print("Entering position hold mode")
        return self.position_hold_active


_controller = StabilityController()

def correct_drift(gps_error, dt: float = 0.02):
    return _controller.correct_drift(gps_error, dt=dt)

def adjust_altitude(current_altitude: float, target_altitude: float, dt: float = 0.02):
    return _controller.adjust_altitude(current_altitude, target_altitude, dt=dt)

def hold_position():
    return _controller.hold_position()