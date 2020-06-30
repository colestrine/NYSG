"""
main is the driver script for the rapsberry Pi. It runs continously, reading
in the sensor data, running the ML algorithm, and then responds with an output.
Along the way, it logs data as well.
"""

# -------- IMPORTS  -------------
import smbus2
import RPi.GPIO

# -------- OTHER EXTERNAL IMPORTS ------
import time


# ------ CUSTOM CLASSES ---------
from sensor_class import *
from peripheral_class import *


# ------ CONSTANTS ------------
# interval is the amount of time between different sampling from the greenhouse
INTERVAL = 60


# -------- INITIALIZE --------


def ml_wrapper():
    return


# --------- EVENT LOOP DRIVER --------
def event_loop():
    pass
