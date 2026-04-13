from ..motors import get_motor_status as _get_motor_status


def read_motor_status():
    """Read current motor controller status and PWM state."""
    return _get_motor_status()
