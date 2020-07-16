"""
alert deals with possible alert messages
"""

# ---------- IMPORTS ----------------------
import random  # for testing
import datetime
import time

# --------- CUSTOM IMPORTS ---------------
import pin_constants
from log import init_log, log, MAX_SIZE


# --------- CONSTANTS FOR ALERTS ---------

WATER_LEVEL = 100
ALERT_LOG_PATH = "alert_log.json"
N_TEST_ITER = 100

# --------- TEST RUNNER ENVIRONMENT VARS --------
RUN_TEST = False


# --------- HELPERS ---------------------


def alert_message_generator():
    """
    alert_message_generator(water_level) is the approrpiate alert for water level being low
    REQUIRES: water level is low
    """
    return "Water Level is Low"


def log_alert(alert_message_dict, alert_path=ALERT_LOG_PATH):
    """
    log_alert(alert_message_dict) logs an alert_message_Dict
    """
    log(ALERT_LOG_PATH, alert_message_dict, MAX_SIZE)


# ---------- MAIN -----------------------


def alert(water_level, alert_path=ALERT_LOG_PATH):
    """
    alert(water_level) raises an alert based on the current water level
    logs alert
    RETURNS None i
    """
    # get time
    now = datetime.datetime.now()
    # add second and microsecond
    current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
    time_dict = {}

    alert_dict = {}
    if water_level < WATER_LEVEL:
        alert_dict["water_level"] = alert_message_generator()
    else:
        alert_dict["water_level"] = None

    time_dict[current_time] = alert_dict
    log_alert(time_dict, alert_path)
    return

# ----------- DEBUGGING ----------------


def check_alert_works(n_iter, log_path):
    """
    check_alert_works(n_iter) checks that alerts are processed and logged properly
    over n_iters at log_path to log data
    """
    for _ in range(n_iter):
        alert(random.randint(0, WATER_LEVEL * 2), log_path)


# ----------- MAIN (FOR DEBUGGING) -----------------

if __name__ == "__main__":
    if RUN_TEST:
        # for debugging whether alert logs properly
        init_log(ALERT_LOG_PATH)
        check_alert_works(N_TEST_ITER, ALERT_LOG_PATH)
