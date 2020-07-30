"""
utilities contains utilities for using the interface fioles
"""


def manual_action_to_activity(action_dict):
    """
    manual_action_to_activity(action_amount) converts an action level into 1 
    or 0 based on the amount >0 or not
    """
    new_dict = {key: (1 if action_dict[key] != "none" else 0) for key in action_dict}
    return new_dict
