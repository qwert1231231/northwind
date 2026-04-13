from ..obstacle_handling import detect_obstacle


def scan_for_obstacle(sensor_packet):
    """Check sensor input for a nearby obstacle."""
    return detect_obstacle(sensor_packet)
