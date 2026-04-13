from ..navigation import set_destination


def set_target_coordinate(lat, lon):
    """Store a target GPS coordinate for the drone mission."""
    return set_destination(lat, lon)
