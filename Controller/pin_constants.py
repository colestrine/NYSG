# ------- IMPORTS --------

import json
import pickle
from datetime import datetime, time


# -----I2C constants --------

SDA = 3
SCL = 5

TEMP_ADDR = 0x40
MOISTURE_ADDR = 0x36
LIGHT_ADDR = 0x10
CO2_ADDR = 0x58

# ------- DEPRECATED ---------
TEMP_REGISTER = 0xE7
LIGHT_REGISTER = 0x04
# ------- DEPRECATED ---------

AMBIENT_LIGHT_READ = 0x04
LIGHT_READ = 0x05

MEASURE_TEMP_REGISTER_NO_HOLD = 0xF3
MEASURE_TEMP_REGISTER_HOLD = 0xE3
MEASURE_RH_REGISTER_NO_HOLD = 0xF5
MEASURE_RH_REGISTER_HOLD = 0xE5
READ_TEMP_HUMID = 0xE7
RESET_TEMP_HUMID = 0xEF

# ---- MODIFY SENSOR ADDRS FOR WHICH SENSORS ARE USED ----
SENSOR_ADDRS = [
    TEMP_ADDR,
    MOISTURE_ADDR,
    LIGHT_ADDR,
    CO2_ADDR,
]

I2C_PORT_NUM = 1

# ----- Peripheral Constants --------

VENT = 13
LED = 26
VALVE = 12
HEAT = 16

BURST = 10  # in seconds

NO_ACTION = 0
BIG_DECREASE = 15
SMALL_DECREASE = 30
SMALL_INCREASE = 45
BIG_INCREASE = 60

DC = 50 # percent %
FREQ = 128 # hZ

# ------- LIGHT CONSTANTS ---------
LIGHT_ON_TIME = 9 * 60 * 60  # time on in seconds
START_LIGHT = (6, 30)  # when light starts as a tuple using 24 hour day
END_LIGHT = (20, 30)  # when light ends as a tuple using 24 hour day


# -------- ALERT CONSTANTS ------
ALERT_INTERVAL = 1 * 60 * 60  # time in seconds


# ------- lOG LOCATIONS -------------


TEMPERATURE_LOG_PATH = "temperature_log.json"
ALL_DATA_LOG_PATH = "all_data_log.json"


# --------- LOGGING UTILITIES FOR DEBUGGING PINS -------------


def load_data(path):
    """
    load_data(path) loads data from path in a json format with read only, 
    NOT READ BYTES

    returns obj
    """
    fp = open(path, "r")
    obj = json.load(fp)
    fp.close()
    return obj


def dump_data(obj, path):
    """
    dump_data loads obj into path in JSON format
    uses WRITe, not WRITE BYTES
    """
    fp = open(path, "w")
    json.dump(obj, fp)
    fp.close()


def load_pickled_data(path):
    """
    load_data(path) loads data from path in a pickle format with read only, 
    USES READ BYTES

    returns obj
    """
    fp = open(path, "rb")
    obj = pickle.load(fp)
    fp.close()
    return obj


def dump_pickled_data(obj, path):
    """
    dump_data loads obj into path in pickle format
    uses WRITE BYTES
    """
    fp = open(path, "wb")
    pickle.dump(obj, fp)
    fp.close()
