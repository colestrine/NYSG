"""
[main] is the driver script for the rapsberry Pi. It runs continously, reading
in the sensor data, running the ML algorithm, and then responds with an output.
Along the way, it logs data as well.

DEPENDENCIES:
- smbus2 for input sensors
- RPi.GPIO for output peripherals
"""

# -------- IMPORTS  -------------
import smbus2
import RPi.GPIO

# -------- OTHER EXTERNAL IMPORTS ------
import time


# ------ CUSTOM CLASSES ---------
from sensor_class import *
from peripheral_class import *
import pin_constants


# ------ CONSTANTS ------------
# interval is the amount of time between different sampling from the greenhouse
WAIT_INTERVAL_SECONDS = 60


# -------- OUTSIDE WRAPPERS --------


def ml_adapter(args_dict):
    """
    ml_adapter() is a wrapper/adapter to fit for the ml functions
    [args_dict] is a dictionary of arguments used for the ml_fucntion

    TODO:
    Call ml_function(s) here
    TODO:
    Change arguments to correct result, and adapt the final results
    """
    return {"valve": True, "heat": True, "light": True, "fan": 20}

# -------- OUTSIDE WRAPPERS --------


def init():
    """
    init() sets up the controller with appropriate objects
    and calls appropriate set up/init functions to get ready for event loop
    """

    # Dictionary to return args
    ret_dict = {}

    # --- Set Up Sensors ---------

    sensor_channel = create_channel(1)
    light_sensor = LightSensor(
        pin_constants.LIGHT_ADDR, pin_constants.LIGHT_REGISTER, sensor_channel)
    temp_humid_sensor = TempHumiditySensor(
        pin_constants.TEMP_ADDR, pin_constants.TEMP_REGISTER, sensor_channel)
    moisture_sensor = MoistureSensor()
    co2_sensor = Co2Sensor()

    ret_dict["light_sensor"] = light_sensor
    ret_dict["temp_sensor"] = temp_humid_sensor
    ret_dict["moisture_sensor"] = moisture_sensor
    ret_dict["co2_sensor"] = co2_sensor

    # --- Set Up Peripherals -----

    # set mode as board
    GPIO.setmode(GPIO.BOARD)

    valve = SolenoidValve(pin_constants.VALVE)
    heat = HeatPad(pin_constants.HEAT)
    fan = Fan(pin_constants.VENT)
    light = PlantLight(pin_constants.LED)

    ret_dict["valve"] = valve
    ret_dict["heat"] = heat
    ret_dict["fan"] = fan
    ret_dict["light"] = light

    return ret_dict


# --------- EVENT LOOP DRIVER --------


def one_cycle(sensors_dict):
    """
    one_cycle(sensors_peris) carries out reads on one cycle of sensors
    """
    sensor_list = [sensors_dict[key] for key in sensors_dict if key in [
        "light_sensor", "temp_sensor", "moisture_sensor", "co2_sensor"]]
    results_dict = collect_all_sensors(sensor_list)
    return results_dict


def event_loop(init_dict):
    """ 
    event_loop() the main event loop

    [init_dict] is the dictionary of arguments form initialization

    CONTINUES FOREVER
    """
    while True:
        ml_args = one_cycle(init_dict)
        ml_results = ml_adapter(ml_args)
        peripheral_dict = {key: init_dict[key] for key in init_dict if key in [
            "heat", "valve", "fan", "light"]}
        react_all(ml_results, peripheral_dict)
        time.sleep(WAIT_INTERVAL_SECONDS)


# ------- MAIN -------------------


if __name__ == "__main__":
    init_dict = init()
    event_loop(init_dict)
