"""
alert deals with possible alert messages
"""

# ---------- IMPORTS ----------------------

from log import log


# --------- CONSTANTS FOR ALERTS ---------

WATER_LEVEL = 100
ALERT_LOG_PATH = "alert_log.json"

# --------- HELPERS ---------------------


def alert_message_generator():
    """
    alert_message_generator(water_level) is the approrpiate alert for water level being low
    REQUIRES: water level is low
    """
    return "Water Level is Low"

# ---------- MAIN -----------------------


def alert(water_level):
    """
    alert(water_level) raises an alert based on the current water level
    RETURNS None if no alerts raises
    """
    if water_level < WATER_LEVEL:
        return alert_message_generator()
    else:
        return None
