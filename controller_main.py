
""" [main] is the driver script for the rapsberry Pi. It runs continously, reading in the sensor data, running the ML 
algorithm, and then responds with an output. Along the way, it logs data as well. """


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
buckets_dict_limited = {"temperature" : buckets_dict["temperature"], "humidity" : buckets_dict["humidity"],"sunlight" : buckets_dict["sunlight"], "soil_moisture" : buckets_dict["soil_moisture"] }
BUCKETS_ASSOC = convert_bucket_to_assoc(buckets_dict_limited)


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

    print(f'ml_args: {ml_args}')

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
    if healthy_light >= 4:
        return "Full sun"
    elif healthy_light >= 3:
        return "Part sun"
    elif healthy_light >= 2:
        return "Part shade"
    elif healthy_light >= 1:
        return "Full shade"
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

    print(f'goal_state: {goal_state}')

    for key in args_dict:
        ml_args = args_dict[key]
    
    current_state_dict = process_to_ml(ml_args)
    print(f"arg_dict : {args_dict}")
    print(f"current_state_dict : {current_state_dict}")
    curr_t = current_state_dict['temperature']
    curr_h = current_state_dict['humidity']
    curr_m = current_state_dict['soil_moisture']
    curr_l = current_state_dict['sunlight']
    curr_state = machine_learning.State(curr_t, curr_h,
                                        curr_m)

    ml_results = machine_learning.Agent.run(curr_state, goal_state)
    print(f'RAW ML RESULTS: {ml_results}')

    ml_result_dict = process_from_ml(ml_results)

    # add in the light implementation here
    plant_type = light_level_to_plant_type(healthy_light)
    new_light_dict = light(light_dict, light_intensity, plant_type) # used to be curr_l
    light_action = new_light_dict["ACTION"]
    ml_result_dict["light"] = light_action
    
    print(f'ML DECISION: {ml_result_dict}')

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
    light_sensor = LightSensor(i2c_channel)
    temp_humid_sensor = TempHumiditySensor(i2c_channel)
    moisture_sensor = MoistureSensor()

    ret_dict["light_sensor"] = light_sensor
    ret_dict["temp_humidity_sensor"] = temp_humid_sensor
    ret_dict["moisture_sensor"] = moisture_sensor

    # --- Set Up Peripherals -----
    # sets up mode internally as well
    valve = SolenoidValve(pin_constants.VALVE, 20)
    heat = HeatPad(pin_constants.HEAT, 50)
    fan = Fan(pin_constants.VENT, 20)  # inverts duty cycles inside class
    light = PlantLight(pin_constants.LED, 20)

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
    manual_control_dict = {"mode": "machine_learning"}  # TODO: change to ML later
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

    # read from manual control interface
    manual_control = pin_constants.load_data(manual_control_path)
    manual_results = pin_constants.load_data(manual_actions_path)

    # read from email settings
    email_settings = pin_constants.load_data(email_settings_path)

    # read from pwm settings
    pwm_settings = pin_constants.load_data(pwm_settings_path)

    # read from frequency settings
    freq_settings = pin_constants.load_data(freq_settings_path)
    print(f"Frequency_settings: {freq_settings}")
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
        ml_results, new_light_dict = ml_adapter(ml_args, light_dict, light_intensity)
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
        print(f'ml_args: {ml_args}')
        print(f'key: {key}')
        for typ in ml_args[key]:
            new_inner_dict[typ] = convert_to_bucket(
                ml_args[key][typ], typ, BUCKETS_ASSOC)
        log_dict[key] = new_inner_dict
        saved_key = key
    for key in peripheral_actions:
        log_dict[saved_key][key + str("_action")] = peripheral_actions[key]

    log(LOG_PATH, log_dict, max_log_size)

    alert_status = init_dict["alert_status"] 
    water_use = pin_constants.WATER_FLOW_RATE * peripheral_actions["water"] * 15 # 15 second cycle
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
        if action == 0 or action == "off":
            return "off"
        elif action == 1:
            return "big_decrease"
        elif action == 2 or action == "low":
            return "low"
        elif action == 3:
            return "small_increase"
        elif action == 4 or action == "high":
            return "high"
        
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

    print(f"EFFECTS: {put}")

    init_dict["state"] = current_state

    await sleep_task


async def one_cycle_driver(init_dict, manual_control_path=MODE_PATH, manual_actions_path=MANUAL_ACTIONS_PATH, email_settings_path=EMAIL_SETTINGS_PATH, pwm_settings_path=PWM_SETTINGS_PATH, freq_settings_path = FREQUENCY_SETTINGS_PATH, sensor_log_path=SENSOR_LOG, ml_action_log=ML_ACTION_LOG, alert_log=ALERT_LOG, max_log_size=MAX_SIZE, interval=0):
    """
    one_cycle_driver(init_dict_path=INIT_DICT_PICKLE_PATH) does one cycle based on the
    information from init_path

    PRIMARILY INTENDENDED FOR ASYNC USE WITH BASH SCRIPT

    REQIIRES: init_dict has beenm initalized already
    """
  #  init_dict = pin_constants.load_pickled_data(init_dict_path)
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
        while True:
            await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                            alert_log, max_log_size, interval)
    else:
        for _ in range(max_iter):
            # time each loop and tell me how long it takes
            start = timeit.default_timer()

            await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                            alert_log, max_log_size, interval)

            stop = timeit.default_timer()
            execution_time = stop - start
            print("One Loop Executed in "+str(execution_time))


# ------- MAIN -------------------


async def main(n_cycles=None):
    """
    main(n_cycles) runs the controller for n_cycles. If n_cycles is None. 
    runs forever

    IF ONE_CYCLE FLAG is activated, runs only for one loop
    """
    init_dict = init()
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
        GPIO.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"Other exception detected: {e}")
        GPIO.cleanup()
        sys.exit(0)
