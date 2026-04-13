"""Flight control for Northwind drone systems."""

import math
from dataclasses import dataclass
from typing import List, Tuple

from .hal import FlightControllerHAL
from .motors import MotorController
from .sensor_fusion import SensorFusion


@dataclass
class PIDConfig:
    kp: float
    ki: float
    kd: float
    integrator: float = 0.0
    last_error: float = 0.0


class FlightControlSystem:
    """Core flight control loop using hardware abstraction and sensor fusion."""

    def __init__(self, hal: FlightControllerHAL, motor_controller: MotorController, fusion: SensorFusion):
        self.hal = hal
        self.motor_controller = motor_controller
        self.fusion = fusion
        self.roll_pid = PIDConfig(1.0, 0.01, 0.05)
        self.pitch_pid = PIDConfig(1.0, 0.01, 0.05)
        self.yaw_pid = PIDConfig(0.8, 0.005, 0.03)
        self.altitude_pid = PIDConfig(1.2, 0.02, 0.06)
        self.target_roll = 0.0
        self.target_pitch = 0.0
        self.target_yaw = 0.0
        self.target_altitude = 0.0
        self.base_throttle = 1200

    def _clamp_pwm(self, value: int) -> int:
        return max(1000, min(2000, value))

    def _pid_update(self, config: PIDConfig, error: float, dt: float) -> float:
        config.integrator += error * dt
        derivative = (error - config.last_error) / dt if dt > 0 else 0.0
        output = config.kp * error + config.ki * config.integrator + config.kd * derivative
        config.last_error = error
        return output

    def update_sensors(self, dt: float = 0.02) -> dict:
        gps_data = self.hal.read_gps()
        imu_data = self.hal.read_imu()
        fused = self.fusion.estimate_position(gps_data, imu_data, dt)
        fused['heading'] = self.fusion.estimate_heading(imu_data)
        return fused

    def set_motor_speeds(self, motor_pwms: List[int]) -> List[int]:
        if len(motor_pwms) != 4:
            raise ValueError('Exactly 4 motor PWM values are required')
        safe_values = [self._clamp_pwm(int(p)) for p in motor_pwms]
        for index, pwm in enumerate(safe_values):
            self.hal.set_motor_pwm(index, pwm)
        return safe_values

    def set_motor_mixes(self, roll: float, pitch: float, yaw: float, throttle: float) -> List[int]:
        throttle_value = self._clamp_pwm(int(throttle))
        motor_values = [throttle_value] * 4
        motor_values[0] += int(-roll + pitch + yaw)
        motor_values[1] += int(roll + pitch - yaw)
        motor_values[2] += int(roll - pitch + yaw)
        motor_values[3] += int(-roll - pitch - yaw)
        safe_values = [self._clamp_pwm(p) for p in motor_values]
        return self.set_motor_speeds(safe_values)

    def stabilize(self, target_roll: float, target_pitch: float, target_yaw: float, target_altitude: float, dt: float = 0.02) -> List[int]:
        state = self.update_sensors(dt)
        current_altitude = state.get('altitude', 0.0)
        current_heading = state.get('heading', 0.0)

        roll_error = target_roll
        pitch_error = target_pitch
        yaw_error = target_yaw - current_heading
        altitude_error = target_altitude - current_altitude

        roll_pwm = self._pid_update(self.roll_pid, roll_error, dt)
        pitch_pwm = self._pid_update(self.pitch_pid, pitch_error, dt)
        yaw_pwm = self._pid_update(self.yaw_pid, yaw_error, dt)
        altitude_pwm = self._pid_update(self.altitude_pid, altitude_error, dt)

        target_throttle = self.base_throttle + int(altitude_pwm)
        motor_pwms = self.set_motor_mixes(roll_pwm, pitch_pwm, yaw_pwm, target_throttle)
        return motor_pwms

    def estimate_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float]:
        lat_diff = end[0] - start[0]
        lon_diff = end[1] - start[1]
        heading = math.degrees(math.atan2(lon_diff, lat_diff)) % 360
        distance = math.hypot(lat_diff, lon_diff) * 111.0
        return heading, distance, math.hypot(lat_diff, lon_diff)

    def navigate_to(self, target_lat: float, target_lon: float, dt: float = 0.02) -> Tuple[float, float]:
        fused = self.update_sensors(dt)
        current = (fused['latitude'], fused['longitude'])
        heading, distance, _ = self.estimate_route(current, (target_lat, target_lon))
        desired_pitch = min(10.0, distance * 0.5)
        desired_roll = 0.0
        desired_yaw = heading
        desired_altitude = fused['altitude']
        self.stabilize(desired_roll, desired_pitch, desired_yaw, desired_altitude, dt)
        return heading, distance

    def arm(self) -> None:
        self.hal.arm_motors()
        self.base_throttle = 1000

    def disarm(self) -> None:
        self.hal.disarm_motors()
