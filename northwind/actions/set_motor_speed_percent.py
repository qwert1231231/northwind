from ..motors import set_motor_speed as _set_motor_speed


def set_motor_speed_percent(percent):
    """Set the motor output as a percent of the device PWM range."""
    return _set_motor_speed(percent)
