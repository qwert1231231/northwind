from ..navigation import update_position


def refresh_position():
    """Update the current position from simulated GPS/IMU data."""
    return update_position()
