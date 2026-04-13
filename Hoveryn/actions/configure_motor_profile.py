from ..motors import set_hardware_device


def configure_motor_profile(device_type):
    """Select the hardware profile for motor control."""
    return set_hardware_device(device_type)
