"""
[main] is the driver script for the rapsberry Pi. It runs continously, reading
in the sensor data, running the ML algorithm, and then responds with an output.
Along the way, it logs data as well.
"""


# -------- EXTERNAL IMPORTS ------
import time
from datetime import datetime
import pickle
import importlib
import sys


# ------ CUSTOM CLASSES ---------
from sensor_class import LightSensor, TempHumiditySensor, MoistureSensor, create_channel, collect_all_sensors
from peripheral_class import SolenoidValve, HeatPad, Fan, PlantLight, react_all
from log import init_log, log, MAX_SIZE
from alert import alert, ALERT_LOG_PATH
import pin_constants


# --------- MACHINE LEARNING IMPORTS ----------
# from Machine_Learning.reinforcement_learning import Agent, State


# --------- INTERFACE FILES IMPORTS ------------
# from Interface_Files.utilities import manual_action_to_activity
utilities = importlib.import_module('../Interface_Files.utilities')


# ------ CONSTANTS ------------
# interval is the amount of time between different sampling from the greenhouse
WAIT_INTERVAL_SECONDS = 60


SENSOR_LOG = "sensor_log.json"
ML_ACTION_LOG = "ml_action_log.json"
ALERT_LOG = "alert_log.json"
INIT_DICT_PICKLE_PATH = "init_dict_pickle_path.pickle"
MANUAL_CONTROL_PATH = "manual_control_path.json"


# -------- RUN ENVIRONMENT VARIABLES ---------
ONE_CYCLE = True


# -------- OUTSIDE WRAPPERS --------


def process(ml_reaction):
    """
    process(ml_reaction) processes the ml_reaction from the mL-algorithm
    into a usable form
    """
    return


def ml_adapter(args_dict):
    """
    ml_adapter() is a wrapper/adapter to fit for the ml functions
    [args_dict] is a dictionary of arguments used for the ml_fucntion

    TODO:
    Call ml_function(s) here
    TODO:
    Change arguments to correct result, and adapt the final results
    """
    process(None)
    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M")
    final_dict = {}
    final_dict[dt_string] = {"valve": True,
                             "heat": True, "light": True, "fan": 20}
    return final_dict

# -------- INTIALIZATION WRAPPERS --------


def init(dump_init_path=INIT_DICT_PICKLE_PATH):
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
    i2c_channel = create_channel()
    light_sensor = LightSensor(i2c_channel)
    temp_humid_sensor = TempHumiditySensor(i2c_channel)
    moisture_sensor = MoistureSensor()

    ret_dict["light_sensor"] = light_sensor
    ret_dict["temp_humidity_sensor"] = temp_humid_sensor
    ret_dict["moisture_sensor"] = moisture_sensor

    # --- Set Up Peripherals -----
    # sets up mode internally as well
    valve = SolenoidValve(pin_constants.VALVE)
    heat = HeatPad(pin_constants.HEAT)
    fan = Fan(pin_constants.VENT)
    light = PlantLight(pin_constants.LED)

    ret_dict["valve"] = valve
    ret_dict["heat"] = heat
    ret_dict["fan"] = fan
    ret_dict["light"] = light

    # set up logging dictionaries
    init_log(SENSOR_LOG)
    init_log(ML_ACTION_LOG)
    init_log(ALERT_LOG)

    # set up manual control and dump into memory
    manual_control_dict = {"mode": "machine_learning"}
    pin_constants.dump_data(manual_control_dict, MANUAL_CONTROL_PATH)

    # set up init pickle path
    pin_constants.dump_pickled_data(ret_dict, dump_init_path)

    return ret_dict


# --------- EVENT LOOP DRIVER --------


def one_cycle_sensors(sensors_dict):
    """
    one_cycle_sensors(sensors_peris) carries out reads on one cycle of sensors
    """
    sensor_list = [sensors_dict[key] for key in sensors_dict if key in [
        "light_sensor", "moisture_sensor", "temp_humidity_sensor"]]
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


def one_cycle(init_dict, manual_control_path, sensor_log_path, ml_action_log, alert_log, max_log_size, interval):
    """
    Executes one cycle of reading, logging, using decision and rwsponding
    Returns NONE
    """
    # read from manual control interface
    manual_control = pin_constants.load_data(manual_control_path)
    manual_results = pin_constants.load_data(MANUAL_CONTROL_PATH)
    ml_args = one_cycle_sensors(init_dict)
    log(ml_args, sensor_log_path, max_log_size)

    if manual_control["mode"] == "machine_learning":
        ml_results = ml_adapter(ml_args)
        peripheral_actions = one_cycle_peripherals(init_dict, ml_results)
    elif manual_control["mode"] == "manual":
        manual_results = {"now": {}}
        peripheral_actions = one_cycle_peripherals(init_dict, manual_results)

    alert(100, ALERT_LOG_PATH)
    log(peripheral_actions, ml_action_log, max_log_size)
    time.sleep(interval)


def one_cycle_driver(init_dict_path=INIT_DICT_PICKLE_PATH, manual_control_path=MANUAL_CONTROL_PATH, sensor_log_path=SENSOR_LOG, ml_action_log=ML_ACTION_LOG, alert_log=ALERT_LOG, max_log_size=MAX_SIZE, interval=0):
    """
    one_cycle_driver(init_dict_path=INIT_DICT_PICKLE_PATH) does one cycle based on the
    information from init_path

    PRIMARILY INTENDENDED FOR ASYNC USE WITH BASH SCRIPT

    REQIIRES: init_dict has beenm initalized already
    """
    init_dict = pin_constants.load_pickled_data(init_dict_path)
    one_cycle(init_dict, manual_control_path, sensor_log_path, ml_action_log,
              alert_log, max_log_size, interval)


def event_loop(init_dict, manual_control_path, sensor_log_path, ml_action_log, alert_log, max_log_size, interval, max_iter=None):
    """ 
    event_loop() the main event loop

    [init_dict] is the dictionary of arguments form initialization

    if max_iter is None, then continues forefver, else less than max_iter

    CONTINUES FOREVER
    """
    if max_iter == None:
        while True:
            one_cycle(init_dict, manual_control_path, sensor_log_path, ml_action_log,
                      alert_log, max_log_size, interval)
    else:
        for _ in range(max_iter):
            one_cycle(init_dict, manual_control_path, sensor_log_path, ml_action_log,
                      alert_log, max_log_size, interval)


# ------- MAIN -------------------


if __name__ == "__main__":
    init_dict = init(INIT_DICT_PICKLE_PATH)
    if ONE_CYCLE:
        one_cycle_driver()
    else:
        event_loop(init_dict, MANUAL_CONTROL_PATH, SENSOR_LOG, ML_ACTION_LOG,
                   ALERT_LOG, MAX_SIZE, WAIT_INTERVAL_SECONDS, None)


# ------- DEBUGGING -------------------

# in the future, would like to have asynchrnous program report back
# what is being read from the sensor and what the peripherals are being responded
# to
