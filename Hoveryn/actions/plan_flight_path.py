from ..navigation import calculate_route


def plan_flight_path(start, end):
    """Build a simple waypoint flight path from start to end."""
    return calculate_route(start, end)
