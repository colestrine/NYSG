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
    if action == "none":
        return pin_constants.NO_ACTION
    elif action == "big_decrease":
        return pin_constants.BIG_DECREASE
    elif action == "small_decrease":
        return pin_constants.SMALL_DECREASE
    elif action == "small_increase":
        return pin_constants.SMALL_INCREASE
    elif action == "big_increase":
        return pin_constants.BIG_INCREASE


def manual_action_to_activity(action_dict):
    """
    manual_action_to_activity(action_amount) converts an action level into 1
    or 0 based on the amount >0 or not
    """
    # (1 if action_dict[key] != "none" else 0)
    new_dict = {key: translate_action(action_dict[key]) for key in action_dict}
    return new_dict
