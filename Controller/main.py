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
from datetime import datetime


# ------ CUSTOM CLASSES ---------
from sensor_class import *
from peripheral_class import *
from log import log, MAX_SIZE
from alert import alert
import pin_constants


# ------ CONSTANTS ------------
# interval is the amount of time between different sampling from the greenhouse
WAIT_INTERVAL_SECONDS = 60


SENSOR_LOG = "sensor_log.json"
ML_ACTION_LOG = "ml_action_log.json"
ALERT_LOG = "alert_log.json"


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
    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M")
    final_dict = {}
    final_dict[dt_string] = {"valve": True,
                             "heat": True, "light": True, "fan": 20}
    return final_dict

# -------- OUTSIDE WRAPPERS --------


def init():
    """
    init() sets up the controller with appropriate objects
    and calls appropriate set up/init functions to get ready for event loop
    """

    # ------ Dictionary to return args -------
    ret_dict = {}

    # ----- SET UP DICTIONARIES FOR LOGS-----
    pin_constants.dump_data({}, SENSOR_LOG)
    pin_constants.dump_data({}, ML_ACTION_LOG)
    pin_constants.dump_data({}, ALERT_LOG)

    # --- Set Up Sensors ---------

    sensor_channel = create_channel(1)
    light_sensor = LightSensor(
        pin_constants.LIGHT_ADDR, pin_constants.AMBIENT_LIGHT_READ, sensor_channel)
    temp_sensor = TemperatureSensor(
        pin_constants.TEMP_ADDR, pin_constants.READ_TEMP_HUMID, sensor_channel)
    humidity_sensor = HumiditySensor(
        pin_constants.TEMP_ADDR, pin_constants.READ_TEMP_HUMID, sensor_channel)
    moisture_sensor = MoistureSensor()
    co2_sensor = Co2Sensor()

    ret_dict["light_sensor"] = light_sensor
    ret_dict["temp_sensor"] = temp_sensor
    ret_dict["moisture_sensor"] = moisture_sensor
    ret_dict["humidity_sensor"] = humidity_sensor
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


def one_cycle_sensors(sensors_dict):
    """
    one_cycle_sensors(sensors_peris) carries out reads on one cycle of sensors
    """
    sensor_list = [sensors_dict[key] for key in sensors_dict if key in [
        "light_sensor", "temp_sensor", "moisture_sensor", "co2_sensor", "humidity_sensor"]]
    results_dict = collect_all_sensors(sensor_list)
    return results_dict


def one_cycle_peripherals(init_dict, ml_results):
    """
    one_cycle_peripherals(ml_results) executes actions on peripherals from ml_results
    with the peripherals from init_dict

    RETURNS: peripheral_actions from ML algorithm
    """
    for time in ml_results:
        peripheral_actions = ml_results[time]
        peripheral_dict = {key: init_dict[key] for key in init_dict if key in [
            "heat", "valve", "fan", "light"]}
        react_all(peripheral_actions, peripheral_dict)
        # return immeidately as ml_results is a dict with only 1 key
        return peripheral_actions


def one_cycle(init_dict, sensor_log_path, ml_action_log, alert_log, max_log_size, interval):
    """
    Executes one cycle of reading, logging, using decision and rwsponding 
    Returns NONE
    """
    ml_args = one_cycle_sensors(init_dict)
    log(ml_args, sensor_log_path, max_log_size)
    ml_results = ml_adapter(ml_args)
    peripheral_actions = one_cycle_peripherals(init_dict, ml_results)
    alert_message = alert(100)
    if alert_message != None:
        log(alert_message, alert_message, max_log_size)
    log(peripheral_actions, ml_action_log, max_log_size)
    time.sleep(interval)


def event_loop(init_dict, sensor_log_path, ml_action_log, alert_log, max_log_size, interval, max_iter):
    """ 
    event_loop() the main event loop

    [init_dict] is the dictionary of arguments form initialization

    if max_iter is None, then continues forefver, else less than max_iter

    CONTINUES FOREVER
    """
    if max_iter == None:
        while True:
            one_cycle(init_dict, sensor_log_path, ml_action_log,
                      alert_log, max_log_size, interval)
    else:
        for _ in range(max_iter):
            one_cycle(init_dict, sensor_log_path, ml_action_log,
                      alert_log, max_log_size, interval)


# ------- MAIN -------------------


if __name__ == "__main__":
    init_dict = init()
    event_loop(init_dict, SENSOR_LOG, ML_ACTION_LOG,
               ALERT_LOG, MAX_SIZE, WAIT_INTERVAL_SECONDS, None)
