from ..motors import stop_motor as _stop_motor


def stop_motor():
    """Stop the motor output and return to the minimum PWM state."""
    return _stop_motor()
