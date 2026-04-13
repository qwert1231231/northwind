"""
Decision module for Northwind drone library.
Uses rule-based logic for mission and obstacle handling.
"""


def choose_action(state: str) -> str:
    if state == 'obstacle_detected':
        action = 'avoid'
    elif state == 'low_battery':
        action = 'return_home'
    elif state == 'target_reached':
        action = 'hover'
    elif state == 'emergency':
        action = 'land'
    else:
        action = 'continue'

    print(f"Decision selected '{action}' for state '{state}'")
    return action


def predict_next_move(state: str = 'normal') -> str:
    if state == 'obstacle_detected':
        return 'avoid'
    if state == 'low_battery':
        return 'return_home'
    if state == 'target_reached':
        return 'hover'
    return 'continue'