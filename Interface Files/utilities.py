"""
utilities contains utilities for using the interface fioles
"""

# --------IMPORTS ---------
from Controller import pin_constants

# ---------CODE ---------


def translate_action(action):
    """
    translate_action(action) translates the manual action to the burst time
    """
    if action == "none" or action == "off":
        return 0
    elif action == "big_decrease":
        return 1
    elif action == "small_decrease" or action == "low":
        return 2
    elif action == "small_increase":
        return 3
    elif action == "big_increase" or action == "high":
        return 4


def manual_action_to_activity(action_dict):
    """
    manual_action_to_activity(action_amount) converts an action level into 1
    or 0 based on the amount >0 or not
    """
    # (1 if action_dict[key] != "none" else 0)
    new_dict = {key: translate_action(action_dict[key]) for key in action_dict}
    return new_dict
