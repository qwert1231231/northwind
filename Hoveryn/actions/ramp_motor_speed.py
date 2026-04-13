from ..motors import ramp_motor_speed as _ramp_motor_speed


def ramp_motor_speed(target_percent, step=5.0, delay=0.05):
    """Ramp motor speed smoothly to a target percent."""
    return _ramp_motor_speed(target_percent, step=step, delay=delay)
