
""" [main] is the driver script for the rapsberry Pi. It runs continously, reading in the sensor data, running the ML
algorithm, and then responds with an output. Along the way, it logs data as well.
"""


# -------- EXTERNAL IMPORTS ------
import time
from datetime import datetime
import pickle
import importlib
import sys
import RPi.GPIO as GPIO

# -------- ASYNCHRONOUS IMPORTS ----------
import asyncio
import timeit


# ------ CUSTOM CLASSES ---------
from Controller.sensor_class import LightSensor, TempHumiditySensor, MoistureSensor, create_channel, collect_all_sensors
from Controller.peripheral_class import SolenoidValve, HeatPad, Fan, PlantLight, react_all
from Controller.log import init_log, log, MAX_SIZE
from Controller.alert import alert, ALERT_LOG_PATH, AlertStatus
from Controller import pin_constants


# ------ LIGHTS IMPORTS ----------
from Lights.light_control import light, startdict


# --------- MACHINE LEARNING IMPORTS ----------
machine_learning = importlib.import_module(
    'Machine Learning.reinforcement_learning-static')
transition = importlib.import_module('Machine Learning.transition-static')


# --------- INTERFACE FILES IMPORTS ------------
utilities = importlib.import_module('Interface Files.utilities')
interface_constants = importlib.import_module(
    'Interface Files.interface_constants')


# ------ CONSTANTS ------------
# interval is the amount of time between different sampling from the greenhouse
WAIT_INTERVAL_SECONDS = 60


# -------- INTERFACE FILE DEPENDENT IMPORTS -------


HEALTHY_LEVELS_PATH = "Interface Files/healthy_levels.json"
VALUE_BUCKETS_PATH = "Interface Files/value_buckets.json"
SENSOR_LOG = "Interface Files/sensor_log.json"
ML_ACTION_LOG = "Interface Files/ml_action_log.json"
ALERT_LOG = "Interface Files/alert_log.json"
MODE_PATH = "Interface Files/mode.json"
MANUAL_ACTIONS_PATH = "Interface Files/manual_actions.json"
PWM_SETTINGS_PATH = "Interface Files/pwm_settings.json"
LOG_PATH = "Interface Files/log.json"
EMAIL_SETTINGS_PATH = "Interface Files/email_settings.json"
FREQUENCY_SETTINGS_PATH = "Interface Files/freq_settings.json"
INIT_DICT_PICKLE_PATH = "init_dict_pickle_path.pickle"
UPDATE_INTERVAl_PATH = "Interface Files/interval_settings.json"


# ------ UTILITIES AND OTHER CONSTANTS ---------


def convert_bucket_to_assoc(buckets):
    new_dict = {}
    for key in buckets:
        assoc_dict = {}
        for num in buckets[key]:
            high = buckets[key][num]["high"]
            low = buckets[key][num]["low"]
            # correct bounds
            if int(num) == 1:
                low = 0
            elif int(num) == 5:
                high = 100
            assoc_dict[(low, high)] = int(num)
        new_dict[key] = assoc_dict
    return new_dict


buckets_dict = pin_constants.load_data(VALUE_BUCKETS_PATH)
BUCKETS_ASSOC = convert_bucket_to_assoc(buckets_dict)


# -------- RUN ENVIRONMENT VARIABLES ---------
ONE_CYCLE = False
N_CYCLES = None
APPEND = True


# ---------- ML TRAINING VARIABLES --------------
TRAIN_ML = False
TRAIN_ML_COUNTER = 0
TRAIN_ML_PATH = "Machine Learning/Files/actions.json"
ACTIONS_JSON = pin_constants.load_data(TRAIN_ML_PATH)

# add in no light action
for key in ACTIONS_JSON:
    ACTIONS_JSON[key]["light"] = "off"


def convert_ml_training_actions(action):
    if action == "off":
        return 0
    elif action == "low":
        return 2
    elif action == "high":
        return 4


ACTIONS_LIST = [ACTIONS_JSON[key] for key in ACTIONS_JSON]
# convert to a compatible action
for _dict in ACTIONS_LIST:
    for key in _dict:
        _dict[key] = convert_ml_training_actions(_dict[key])


# -------- ML WRAPPERS --------


def convert_to_bucket(arg, _type, bucket_assoc):
    """
    convert_to_bucket(ml_args) converts the ml_args into the proper bucket
    values between 1 and 5, adding proper fractional part
    """
    lower_dict = bucket_assoc[_type]
    for low, high in lower_dict:
        if arg >= int(low) and arg <= int(high) + 1:
            remainder = arg - int(low)
            _range = int(high) - int(low)
            fractional_part = remainder/float(_range)
            converted_val = lower_dict[(low, high)] + fractional_part
            assert converted_val < 6
            rounded_result = round(float(converted_val), 1)
            if rounded_result >= 5.9:
                rounded_result = 5.9
            assert rounded_result <= 5.9
            return rounded_result
    # above highest partition
    if arg >= int(high):
        return 5.9
    return 1.0


def process_to_ml(ml_args):
    """
    process_to_ml(ml_args) converts the ml_args into the proper bucket
    values between 1 and 5
    """
    converted_dict = {}

    for key in ml_args:
        converted_dict[key] = convert_to_bucket(
            ml_args[key], key, BUCKETS_ASSOC)
    return converted_dict


def process_from_ml(ml_reaction):
    """
    process_from_ml(ml_reaction) processes the ml_reaction from the mL-algorithm
    into a usable form of interger values 1 and 0 (on/off)
    """
    new_dict = {}
    for key in ml_reaction:
        new_key = key.replace("_action", "")
        new_dict[new_key] = ml_reaction[key]

    final_dict = utilities.manual_action_to_activity(new_dict)

    return final_dict


def light_level_to_plant_type(healthy_light):
    """
    light_level_to_plant_type(healthy_light) converts the healthy_light level; the goal lioght level
    which is between 05 and 5 to a shadelevel for the light algoriothm
    """
    healthy_light = int(healthy_light)

#  ----------------------- EDIT BELOW HERE -----------------------
# TODO 5.

    # We need to convert the healthy light integer into a string. We do it by comparing the
    # value of healthy light. If healthy light is greater than or equal to 4, return
    # the string "Full Sun"

    # If healthy light is greater or equal to 3 and less than 4, return "Part Sun"

    # If healthy light is greater or equal to 2 and less than 3, return "Part Sun"

    # If healthy light is greater or equal to 1 and less than 2, return "Part Shade"

    # If healthy light is greater or equal to 0 and less than 1, return "Full Sun"

    # Remember how to use if statements, elif statements and booleans.

    # Do not add in an else clause.

# END TODO 5.
#  ----------------------- EDIT ABOVE HERE -----------------------
    raise AssertionError("Not a valid healthy light level")


def ml_adapter(args_dict, light_dict, light_intensity):
    """
    ml_adapter() is a wrapper/adapter to fit for the ml functions
    [args_dict] is a dictionary of arguments used for the ml_fucntion
    """
    healthy_levels_dict = pin_constants.load_data(HEALTHY_LEVELS_PATH)
    healthy_temp = str(int(healthy_levels_dict['temperature']) + .5)
    healthy_humidity = str(int(healthy_levels_dict['humidity']) + .5)
    healthy_moisture = str(int(healthy_levels_dict['soil_moisture']) + .5)
    healthy_light = healthy_levels_dict['sunlight']
    goal_state = machine_learning.State(healthy_temp, healthy_humidity,
                                        healthy_moisture)

    for key in args_dict:
        ml_args = args_dict[key]

    current_state_dict = process_to_ml(ml_args)
    curr_t = current_state_dict['temperature']
    curr_h = current_state_dict['humidity']
    curr_m = current_state_dict['soil_moisture']
    curr_l = current_state_dict['sunlight']
    curr_state = machine_learning.State(curr_t, curr_h,
                                        curr_m)

    ml_results = machine_learning.Agent.run(curr_state, goal_state)

    ml_result_dict = process_from_ml(ml_results)

    # add in the light implementation here
    plant_type = light_level_to_plant_type(healthy_light)
    new_light_dict = light(light_dict, light_intensity,
                           plant_type)  # used to be curr_l
    light_action = new_light_dict["ACTION"]
    ml_result_dict["light"] = light_action

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%-S")
    final_dict = {}
    final_dict[dt_string] = ml_result_dict

    return final_dict, new_light_dict

# -------- INTIALIZATION WRAPPERS --------


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

    i2c_channel = create_channel()

    # ----------------------- EDIT BELOW HERE -----------------------
    # TODO 2.
    #
    # Let us create the sensors that we need for this project.

    # We need a light sensor, temperature-humidity sensor and moisture sensor.
    # You can create these objects with the constructors: LightSensor, TempHumiditySensor, MoistureSensor,
    # To get more information for each constructior, read the module code in
    # folder Controller and looking in file sensor_class.py

    # For the light sensor, use the i2c_channel that was created before this section
    # of code. Similarly, use the i2c_channel for the TempHumidity Sensor.
    # The Moisture Sensor needs to arguments to be called.
    # Save the sensors to variables named light_sensor, temp_humid_sensor and moisture_sensor
    # respectively.

    # END TODO 2.
    # ----------------------- EDIT ABOVE HERE -----------------------

    ret_dict["light_sensor"] = light_sensor
    ret_dict["temp_humidity_sensor"] = temp_humid_sensor
    ret_dict["moisture_sensor"] = moisture_sensor

    # --- Set Up Peripherals -----

    # ----------------------- EDIT BELOW HERE -----------------------
    # TODO 3.

    # Let us create the peripherals for this project.

    # We need a Solenoid Valve, Heat Pad, Fan and Plant Light. These are given by
    # the constructors SolenoidValve, HeatPad, Fan, and PlantLight. Each of these takes
    # in a pin number. The pins are:
    # Solenoid Valve: pin_constants.VALVE
    # Heat Pad: pin_constants.HEAT,
    # Fan: pin_constants.VENT,
    # PlantLight: pin_constants.LED

    # Further, each of the constructors takes in a burst time. Give them all 20
    # second burst times. The burst time is an integer.

    # The first argument to each constructor is the pin number, while the second is
    # the burst time. There are no other arguments.

    # Finally, save eacj peripheral to its own variable. The cariables should be
    # named, respectively, valve, heat, fan and light.

    # END TODO 3.
    # ----------------------- EDIT ABOVE HERE -----------------------

    ret_dict["water"] = valve
    ret_dict["heat"] = heat
    ret_dict["fan"] = fan
    ret_dict["light"] = light

    # set up logging dictionaries
    if not APPEND:
        init_log(SENSOR_LOG)
        init_log(ML_ACTION_LOG)
        init_log(ALERT_LOG)

        init_log(LOG_PATH)

    # set up alert time keeping
    ret_dict["alert_status"] = AlertStatus()

    # set up manual control and dump into memory
    # TODO: change to ML later
    manual_control_dict = {"mode": "machine_learning"}
    pin_constants.dump_data(manual_control_dict, MODE_PATH)

    # set up a random state
    ret_dict["state"] = machine_learning.State(1.0, 1.0, 1.0)

    # set up light dictionary
    ret_dict["light_dict"] = startdict()

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


async def one_cycle_peripherals(init_dict, ml_results, pwm_settings, freq_settings):
    """
    one_cycle_peripherals(ml_results) executes actions on peripherals from ml_results
    with the peripherals from init_dict

    RETURNS: peripheral_actions from ML algorithm
    """
    for time in ml_results:
        peripheral_actions = ml_results[time]
        peripheral_dict = {key: init_dict[key] for key in init_dict if key in [
            "heat", "water", "fan", "light"]}
        await react_all(peripheral_actions, peripheral_dict, pwm_settings, freq_settings)
        # return immeidately as ml_results is a dict with only 1 key
        return peripheral_actions


async def one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log, alert_log, max_log_size, interval):
    """
    Executes one cycle of reading, logging, using decision and rwsponding
    Returns NONE
    """

    # read from update interval settings
    interval_settings = pin_constants.load_data(UPDATE_INTERVAl_PATH)
    # update time in seconds !!!, must be greater than 1 minute (60 sec)
    update_interval_time = int(interval_settings["interval"])
    global TRAIN_ML_COUNTER

    # start task to sleep for one cycle
    sleep_task = asyncio.create_task(asyncio.sleep(update_interval_time))

#  ----------------------- EDIT BELOW HERE -----------------------
# TODO 4.

    # We need to be able to read data from the Interface files. We need to reading
    # in 5 items: the manual control status, the manual actions, the email settings
    # the pwm settings and the frequency settings.

    # TO read in data, call the function load_data. Because load_data is in module
    # pin_constants, you will have to us the module with a dot notation:
    # pin_constants.load_data.

    # Load_data takes in one argument, the path of the interface file you want to read.
    # When you can in load_data, load_data returns to you the read in data.

    # First, read in manual_control_path and save the results of the function to a
    # variable named manual_control.

    # Second, read in manual_actions_path and save the results of the function to a
    # variable named manual_results.

    # Next, read in email_settings_path and save the results of the function to a
    # variable named email_settings.

    # Then, read in pwm_settings_path and save the results of the function to a
    # variable named pwm_settings.

    # Finally, read in freq_settings_path and save the results of the function to a
    # variable named freq_settings.

    # Remember, there are five variables you need to create via 5 function calls.

# END TODO 4.
#  ----------------------- EDIT ABOVE HERE -----------------------

    # get light dict
    light_dict = init_dict["light_dict"]

    ml_args = one_cycle_sensors(init_dict)
    for key in ml_args:
        inner_dict = ml_args[key]
        light_intensity = inner_dict['sunlight']
    log(sensor_log_path, ml_args, max_log_size)

    # ML TRAIN STUFF TO BE REMOVED
    if TRAIN_ML:
        if TRAIN_ML_COUNTER == len(ACTIONS_LIST):
            raise RuntimeError("Stop Execution")
        training_actions = ACTIONS_LIST[TRAIN_ML_COUNTER]
        training_results = {"now": training_actions}
        peripheral_actions = await one_cycle_peripherals(init_dict, training_results, pwm_settings, freq_settings)
        TRAIN_ML_COUNTER += 1
    elif manual_control["mode"] == "machine_learning":
        ml_results, new_light_dict = ml_adapter(
            ml_args, light_dict, light_intensity)
        init_dict["light_dict"] = new_light_dict
        peripheral_actions = await one_cycle_peripherals(init_dict, ml_results, pwm_settings, freq_settings)
    elif manual_control["mode"] == "manual":
        converted_results = utilities.manual_action_to_activity(manual_results)
        manual_results = {"now": converted_results}
        peripheral_actions = await one_cycle_peripherals(init_dict, manual_results, pwm_settings, freq_settings)

    log(ml_action_log, peripheral_actions, max_log_size)

    log_dict = {}
    saved_key = None
    for key in ml_args:
        new_inner_dict = {}
        for typ in ml_args[key]:
            new_inner_dict[typ] = convert_to_bucket(
                ml_args[key][typ], typ, BUCKETS_ASSOC)
        log_dict[key] = new_inner_dict
        saved_key = key
    for key in peripheral_actions:
        log_dict[saved_key][key + str("_action")] = peripheral_actions[key]

    log(LOG_PATH, log_dict, max_log_size)

    alert_status = init_dict["alert_status"]
    water_use = pin_constants.WATER_FLOW_RATE * \
        peripheral_actions["water"] * 15  # 15 second cycle
    alert(water_use, log_dict, alert_status, email_settings, ALERT_LOG)

    # handle the logging for ML learning
    for key in (ml_args):
        processed_args = process_to_ml(ml_args[key])
        for sensor in processed_args:
            if sensor == "temperature":
                temp = processed_args[sensor]
            elif sensor == "humidity":
                humid = processed_args[sensor]
            elif sensor == "soil_moisture":
                moist = processed_args[sensor]

    current_state = machine_learning.State(temp, humid, moist)

    def convert_action(action):
        pass

#  ----------------------- EDIT BELOW HERE -----------------------
# TODO 6.
        # We need to convert action to a string. Action can be an integer between 0 and
        # 4 inclusive, or the string "low" or "high".capitalize

        # If action is 0 or it is the string "off", return the string "off".

        # If action is 1 return the string "big_decrease".

        # If action is 2 or it is the string "low", return the string "low".

        # If action is 3 return the string "small_increase".

        # If action is 4 or it is the string "high", return the string "high".

        # Use your boolean comparison equality operation, == , the double equals,
        # as well as if-elif statements. Also return strings inside the if statements.
# END TODO 6.
#  ----------------------- EDIT ABOVE HERE -----------------------

    for key in peripheral_actions:
        if key == "water":
            water = convert_action(peripheral_actions[key])
        elif key == "heat":
            heat = convert_action(peripheral_actions[key])
        elif key == "fan":
            fan = convert_action(peripheral_actions[key])
    action_set = transition.ActionSet(water, fan, heat)

    put = transition.EffectSet.putEffect(
        action_set, init_dict["state"], current_state)

    init_dict["state"] = current_state

    await sleep_task


async def one_cycle_driver(init_dict, manual_control_path=MODE_PATH, manual_actions_path=MANUAL_ACTIONS_PATH, email_settings_path=EMAIL_SETTINGS_PATH, pwm_settings_path=PWM_SETTINGS_PATH, freq_settings_path=FREQUENCY_SETTINGS_PATH, sensor_log_path=SENSOR_LOG, ml_action_log=ML_ACTION_LOG, alert_log=ALERT_LOG, max_log_size=MAX_SIZE, interval=0):
    """
    one_cycle_driver(init_dict_path=INIT_DICT_PICKLE_PATH) does one cycle based on the
    information from init_path

    PRIMARILY INTENDENDED FOR ASYNC USE WITH BASH SCRIPT

    REQIIRES: init_dict has beenm initalized already
    """
    await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                    alert_log, max_log_size, interval)


async def event_loop(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log, alert_log, max_log_size, interval, max_iter=None):
    """
    event_loop() the main event loop

    [init_dict] is the dictionary of arguments form initialization

    if max_iter is None, then continues forefver, else less than max_iter

    CONTINUES FOREVER
    """
    if max_iter == None:
        pass
        #  ----------------------- EDIT BELOW HERE -----------------------
        # TODO 7.

        # In this branch of the if statement, we want the code to runforever. We
        # can use a while loop with true as the guard. Write in the guard. Then
        # paste in the given code below to call the function to run inside the while loop.
        # You do not need to know what await does. Just paste the code indented
        # inside the while loop body.

        # Given code:
        # await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
        #                 alert_log, max_log_size, interval)

        # END TODO 7
        # ----------------------- EDIT ABOVE HERE -----------------------

    else:
        pass

        #  ----------------------- EDIT BELOW HERE -----------------------
        # TODO 8.

        # In this branch of the if statement, we want the code to for a
        # certain number of iterations, max_iter, specifically. max_iter is an integer
        # representing how many iterations to run. We can use a for loop.
        #  We want you to fill in the for loop guard. Create an iteration variable.
        # Use range to make sure you iterate for max_iter iterations.
        # Paste in the given code below to call the function to run inside the for loop.
        # You do not need to know what await does. Just paste the code indented
        # inside the for loop body.

        # Given code:
        # await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
        #                   alert_log, max_log_size, interval)

        # END TODO 8
        # ----------------------- EDIT ABOVE HERE -----------------------

# ------- MAIN -------------------


async def main(n_cycles=None):
    """
    main(n_cycles) runs the controller for n_cycles. If n_cycles is None.
    runs forever

    IF ONE_CYCLE FLAG is activated, runs only for one loop
    """

    # ----------------------- EDIT BELOW HERE -----------------------
    # TODO 1.: WE NEED TO INITIALIZE VARIABLE init_dict WITH A VALUE. YOU WILL NEED TO CALL FUNCTION
    # init TO BE ABLE TO INITIALIZE THE VARIABLE. REMEMBER HOW TO CALL A FUNCTION?
    # NOTE: init is a function with no arguments.
    # END TODO 1.:
    # ----------------------- EDIT ABOVE HERE -----------------------

    if ONE_CYCLE:
        await one_cycle_driver(init_dict)
    else:
        await event_loop(init_dict, MODE_PATH, MANUAL_ACTIONS_PATH, EMAIL_SETTINGS_PATH, PWM_SETTINGS_PATH, FREQUENCY_SETTINGS_PATH, SENSOR_LOG, ML_ACTION_LOG,
                         ALERT_LOG, MAX_SIZE, WAIT_INTERVAL_SECONDS, n_cycles)


# -------- MAIN RUNNER --------------


if __name__ == "__main__":
    print('controller starting...')

    try:
        asyncio.run(main(N_CYCLES))
    except (KeyboardInterrupt, SystemExit):
        print("Interrupt detected")
        sys.exit(0)
    except Exception as e:
        print(f"Other exception detected: {e}")
        sys.exit(0)
