# ------- IMPORTS --------

import json


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

VENT = 33
LED = 37
VALVE = 32
HEAT = 37

# ------- lOG LOCATIONS -------------


TEMPERATURE_LOG_PATH = "temperature_log.json"
ALL_DATA_LOG_PATH = "all_data_log.json"


# --------- LOGGING -------------


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
