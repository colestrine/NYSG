"""
alert deals with possible alert messages
"""

# ---------- IMPORTS ----------------------
import datetime
import time


# --------- EMAIL IMPORTs ---------------
import json
import email
import smtplib
import ssl


# ---------- TESTING IMPORTS ----------------------
import random  # for testing
import sys


# --------- CUSTOM IMPORTS ---------------
from Controller import pin_constants
from Controller.log import init_log, log, MAX_SIZE


# ---------- EMAIL CONSTANTS -----------
CONFIG_PATH = "Controller/configuration.json"
fp = open(CONFIG_PATH, "r")
CONFIG = json.load(fp)
fp.close()
PASSWORD = CONFIG["email_password"]
EMAIL_ADDR = CONFIG["email_address"]
RECEIVER_EMAIL_ADDRESSES = CONFIG["receiver_email_address"]
SSL_PORT = 465  # for SSl
DEBUG_PORT = 1025


# --------- CONSTANTS FOR ALERTS ---------

WATER_LEVEL = 100
ALERT_LOG_PATH = "alert_log.json"
N_TEST_ITER = 100


# --------- TEST RUNNER ENVIRONMENT VARS --------
num_cli_args = len(sys.argv)
if num_cli_args <= 1:
    RUN_TEST = False
else:
    try:
        run_test = True if sys.argv[1].strip().lower() == "true" else False
        RUN_TEST = run_test
    except:
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
    log(alert_path, alert_message_dict, MAX_SIZE)


# --------- EMAIL ALERT SYSTEM------------

def generate_message(log_dict):
    time_key = None
    for key in log_dict:
        time_key = key
        break

    log_data = log_dict[time_key]

    subject = "Subject: NYSG Update @ " + str(time_key) + "\n\n"
    body = " ".join([str(key) + " : " + str(log_data[key])
                     for key in log_data])
    message = subject + body
    return message


def send_email(email_address, email_password, receiver_emails, log_dict, ssl_port):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Generate message
    message = generate_message(log_dict)

    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
        server.login(email_address, email_password)
        for receiver_email in receiver_emails:
            server.sendmail(email_address, receiver_email, message)


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


# ---------- TEST EMAIL --------------


def test_email():
    test_log_dict = {}
    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%-S")
    test_log_dict[dt_string] = {"sunlight": 1.2141250000000001,
                                "temperature": 3.6958802897135405,
                                "humidity": 3.9864832560221353,
                                "soil_moisture": 2.1924116593388705,
                                "water_action": 0,
                                "fan_action": 1,
                                "heat_action": 0,
                                "light_action": 0}
    send_email(EMAIL_ADDR, PASSWORD,
               RECEIVER_EMAIL_ADDRESSES, test_log_dict, DEBUG_PORT)


# ----------- MAIN (FOR DEBUGGING) -----------------
if __name__ == "__main__":
    if RUN_TEST:
        # for debugging whether alert logs properly
        init_log(ALERT_LOG_PATH)
        check_alert_works(N_TEST_ITER, ALERT_LOG_PATH)
