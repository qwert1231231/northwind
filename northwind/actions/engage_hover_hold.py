from ..stability import hold_position


def engage_hover_hold():
    """Hold the current position in the air using stabilization control."""
    return hold_position()
