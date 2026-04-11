"""
Motor control module for Northwind drone library.
Provides PWM speed control and hardware device profiles for ESP32, Arduino, and generic drone controllers.
"""

import time
from typing import Literal

HardwareDevice = Literal['esp32', 'arduino', 'drone']

HARDWARE_PROFILES = {
    'esp32': {
        'min_pwm': 0,
        'max_pwm': 255,
        'frequency': 1000,
        'description': 'ESP32 PWM motor driver profile',
    },
    'arduino': {
        'min_pwm': 0,
        'max_pwm': 255,
        'frequency': 490,
        'description': 'Arduino PWM motor driver profile',
    },
    'drone': {
        'min_pwm': 1000,
        'max_pwm': 2000,
        'frequency': 400,
        'description': 'Generic drone ESC PWM control profile',
    },
}


class MotorController:
    """Motor controller abstraction for PWM-based motor speed and hardware device support."""

    def __init__(self, device_type: HardwareDevice = 'drone'):
        self.device_type = None
        self.profile = None
        self.current_pwm = 0
        self.target_speed = 0.0
        self.enabled = False
        self.set_device(device_type)

    def set_device(self, device_type: str):
        """Configure the motor controller for a supported device profile."""
        if device_type not in HARDWARE_PROFILES:
            raise ValueError(
                f"Unsupported hardware device '{device_type}'. "
                f"Supported devices: {', '.join(HARDWARE_PROFILES)}"
            )

        self.device_type = device_type
        self.profile = HARDWARE_PROFILES[device_type]
        self.current_pwm = self.profile['min_pwm']
        self.target_speed = 0.0
        self.enabled = False
        print(f"Motor controller configured for {device_type.upper()}")
        return self.profile

    def _validate_pwm(self, pwm: float):
        if not isinstance(pwm, (int, float)):
            raise TypeError('PWM value must be a number')
        if pwm < self.profile['min_pwm'] or pwm > self.profile['max_pwm']:
            raise ValueError(
                f"PWM value must be between {self.profile['min_pwm']} "
                f"and {self.profile['max_pwm']} for device '{self.device_type}'"
            )

    def set_speed_pwm(self, pwm: float):
        """Set motor speed directly using a PWM value."""
        self._validate_pwm(pwm)
        self.current_pwm = int(pwm)
        self.target_speed = self._pwm_to_percent(self.current_pwm)
        self.enabled = self.current_pwm > self.profile['min_pwm']
        print(
            f"Motor speed set to PWM={self.current_pwm} "
            f"({self.target_speed:.1f}% for {self.device_type})"
        )
        return self.current_pwm

    def set_speed_percent(self, percent: float):
        """Set motor speed as a percent of full range."""
        if not isinstance(percent, (int, float)):
            raise TypeError('Speed percent must be a number')
        if percent < 0 or percent > 100:
            raise ValueError('Speed percent must be between 0 and 100')

        range_size = self.profile['max_pwm'] - self.profile['min_pwm']
        pwm_value = int(self.profile['min_pwm'] + (percent / 100.0) * range_size)
        return self.set_speed_pwm(pwm_value)

    def ramp_speed(self, target_percent: float, step: float = 5.0, delay: float = 0.05):
        """Smoothly ramp motor speed from current value to a target percent."""
        if not isinstance(target_percent, (int, float)):
            raise TypeError('Target percent must be a number')
        if target_percent < 0 or target_percent > 100:
            raise ValueError('Target percent must be between 0 and 100')
        if step <= 0:
            raise ValueError('Step must be positive')
        if delay < 0:
            raise ValueError('Delay must be non-negative')

        start_percent = self._pwm_to_percent(self.current_pwm)
        direction = 1 if target_percent > start_percent else -1
        current_percent = start_percent

        while (direction > 0 and current_percent < target_percent) or (
            direction < 0 and current_percent > target_percent
        ):
            current_percent += direction * step
            if direction > 0 and current_percent > target_percent:
                current_percent = target_percent
            if direction < 0 and current_percent < target_percent:
                current_percent = target_percent

            self.set_speed_percent(current_percent)
            time.sleep(delay)

        print(f"Ramped motor speed to {target_percent:.1f}%")
        return self.current_pwm

    def stop(self):
        """Stop the motor by setting PWM to the device minimum."""
        return self.set_speed_pwm(self.profile['min_pwm'])

    def get_status(self):
        """Return the motor controller state, including current PWM and enabled status."""
        status = {
            'device_type': self.device_type,
            'current_pwm': self.current_pwm,
            'target_speed_percent': self.target_speed,
            'enabled': self.enabled,
            'profile': self.profile.copy(),
        }
        print(f"Motor status: {status}")
        return status

    def _pwm_to_percent(self, pwm_value: float) -> float:
        range_size = self.profile['max_pwm'] - self.profile['min_pwm']
        if range_size == 0:
            return 0.0
        return float((pwm_value - self.profile['min_pwm']) / range_size * 100.0)


# Convenience singleton for direct package usage
_motor_controller = MotorController()


def set_hardware_device(device_type: str):
    return _motor_controller.set_device(device_type)


def set_motor_speed_pwm(pwm: float):
    return _motor_controller.set_speed_pwm(pwm)


def set_motor_speed(percent: float):
    return _motor_controller.set_speed_percent(percent)


def ramp_motor_speed(target_percent: float, step: float = 5.0, delay: float = 0.05):
    return _motor_controller.ramp_speed(target_percent, step=step, delay=delay)


def stop_motor():
    return _motor_controller.stop()


def get_motor_status():
    return _motor_controller.get_status()
