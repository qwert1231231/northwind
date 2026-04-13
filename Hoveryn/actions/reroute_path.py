from ..obstacle_handling import recalculate_path


def reroute_path():
    """Rebuild the flight path after obstacle avoidance."""
    return recalculate_path()
