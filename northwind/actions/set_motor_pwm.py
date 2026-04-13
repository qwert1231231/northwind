from ..motors import set_motor_speed_pwm as _set_motor_speed_pwm


def set_motor_pwm(pwm_value):
    """Set the motor output directly using a PWM value."""
    return _set_motor_speed_pwm(pwm_value)
