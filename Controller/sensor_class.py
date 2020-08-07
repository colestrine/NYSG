"""
sensor_class includes information relating to the sensors
for the greenhourse:
    - LightSensor
    - HumiditySensor
    - MoistureSensor
    - TemperatureSensor

High level classes to abstract away complications are given
to the students to use.

PACKAGE REQUIREMENTS:
- gpiozero: used to handle the moisture sensor as an SPI Driver
- time (used for time and delays)
- json (used to log read in data from sensors)
- pin_constants [custom]: holds pin data for I2C communication protocols
- busio and board - used for Adafruit I2C channels
- adafruit_veml7700 used for the Adafruit light sensor
- adafruit_si7021 used for the Adafruit temperaure and humidity sensor
- random, datetime, sys, log : used for testing and randomization purposes

MANUAL INSTALLATION:
- pip3 install adafruit_veml7700
    You will need to run the above command to use the adafruit light sensor

- pip3 install adafruit_si7021
    You will need to run the above command to use the adafruit temperature
    and humidity sensor

AUTOMATIC INSTALLATION:
in terminal, run
pip3 install -r requirements.txt
"""

# ----- ADA FRUIT SENSOR IMPORTS -----------------
import busio
import board

import Adafruit_PureIO
import adafruit_si7021
import adafruit_veml7700


# ----- NON ADA FRUIT IMPORTS ------
from gpiozero import MCP3001


# ------- OTHER IMPORTS -------
import time
from datetime import datetime


# -------- CUSTOM IMPORTS --------
from Controller import pin_constants


# -------- TEST IMPORTS ----------
import random
import datetime
import sys
from Controller import log

MAX_LIGHT_DIVISOR = 15000
DRY_SOIL = .7
WET_SOIL = .4

# ------- TEST CONSTANTS ----------
N_SENSORS = 4
N_ITER = 10
SENSOR_LOG_TEST = "SENSOR_LOG_TEST.json"

num_cli_args = len(sys.argv)
if num_cli_args <= 1:
    RUN_TEST = False
else:
    try:
        run_test = True if sys.argv[1].strip().lower() == "true" else False
        RUN_TEST = run_test
    except:
        RUN_TEST = False


# --------- SENSORS ----------------

class LightSensor():
    """
    LightSensor represents a Light Sensor from VISHAY ELECTRONICS

    INSTALLATION: pip3 install adafruit_si7021

    [channel] is the I2C channel of the sensor in the bus
    [sensor] is the i2c sensor object
    """

    def __init__(self, i2c_channel):
        """
        __init__(self, i2c_channel) creates a light sensor object on I2c channel
        [i2c_channel]
        """
        self.channel = i2c_channel
        sensor = adafruit_veml7700.VEML7700(i2c_channel)
        self.sensor = sensor

    def read_light(self):
        """
        read_light(sensor) is the ambient light from the sensor
        """
        return self.sensor.light


class TempHumiditySensor():
    """
    TempHumiditySensor represents a Temperature Sensor and a Humidity Sensor

    INSTALLATION: pip3 install adafruit-circuitpython-veml7700

    [channel] is the I2C channel of the sensor in the bus
    [sensor] is the i2c sensor object
    """

    def __init__(self, i2c_channel):
        self.channel = i2c_channel
        sensor = adafruit_si7021.SI7021(i2c_channel)
        self.sensor = sensor

    def read_temp(self):
        """
        read_temp(sensor) is the fahrenheit temperatue  from the sensor
        """
        def c_to_f(c):
            return 9/5 * c + 32
        return c_to_f(self.sensor.temperature)

    def read_rh(self):
        """
        read_rh(sensor) is the relative humidity  from the sensor
        """
        return self.sensor.relative_humidity


class MoistureSensor():
    """
    MoistureSensor represents an AdaFruit Moisture Sensor

    INSTALLATION: requires mcp_3001 from gpiozero package

    [sensor] is the sensor object for Adafruit
    """

    def __init__(self):
        """
        Creates a Moisture sensor represent an adaFruit Moisture Sensor
        """
        self.sensor = MCP3001()

    def read_moisture(self):
        """
        read_moisture(self) is the moisture read
        """
        unstandardized = self.sensor.value
        # smaller value is low moisture, higher is high moisture, mult by 100 to scale
        standard = soil_conversion(unstandardized)
        return standard


# -------- UTILITIES ------------


def create_channel():
    """
    create_channel(bus_num) creates a channel for I2C communication
    on bus_num bus number.

    WRAPPER FUNCTION for students
    """
    return busio.I2C(board.SCL, board.SDA)

def soil_conversion(raw):
    final = round(100 - (raw - WET_SOIL)* 100/(DRY_SOIL - WET_SOIL))
    if final < 1:
        final = 1
    if final > 99:
        final = 99
    return final

# -------- SUMMARY FUNCTIONS --------


def collect_all_sensors(sensor_list):
    """
    collect_all() collects all the data from all sensors and logs it
    uses the sensors in [sensor_list] which are on the bus object sensor.channel

    Returns the logged data
    """
    ret_dict = {}

    for sensor in sensor_list:
        if type(sensor) == TempHumiditySensor:
            temp = sensor.read_temp()
            rh = sensor.read_rh()
            ret_dict["temperature"] = temp
            ret_dict["humidity"] = rh
        elif type(sensor) == MoistureSensor:
            moisture = sensor.read_moisture()
            ret_dict["soil_moisture"] = moisture
        elif type(sensor) == LightSensor:
            light = sensor.read_light()
            ret_dict["sunlight"] = light

    # get time
    now = datetime.datetime.now()
    # add second and microsecond
    current_time = now.strftime("%d-%m-%Y %H:%M:%-S")

    outer_dict = {}
    outer_dict[current_time] = ret_dict
    return outer_dict


# -------- COMPLEX TESTS ------------


def run_debug(log_path, n_iter):
    """
    run_debug() is used to create a sample bus channel and read from the channel

    logs data in log_path as a json dictionary
    mapping the current time as a string to the temperature recorded

    RECORDS for [n_iter] number of iteractions
    """
    i2c_channel = create_channel()

    light_sensor = LightSensor(i2c_channel)
    temp_humid_sensor = TempHumiditySensor(i2c_channel)
    moisture_sensor = MoistureSensor()

    sensor_list = [light_sensor, temp_humid_sensor, moisture_sensor]

    log_dict = {}
    for _ in range(n_iter):
        output = collect_all_sensors(sensor_list)

        for key in output:
            log_dict[key] = output[key]

    pin_constants.dump_data(log_dict, log_path)


def read_debug_data(log_path, first_few=None):
    """
    read_debug_data(log_path, first_few) reads in debugged daga at the log_path
    for the first_few characgers,
    if first_few is None, greads all and prints all to terminal
    """
    data_dict = pin_constants.load_data(log_path)
    dict_list = [(key, data_dict[key]) for key in data_dict]
    if first_few == None:
        first_few = len(dict_list)
    for i in range(min(len(dict_list), first_few)):
        print(dict_list[i][1])


# ---------- TEST LOGGING FUNCTIONALITY -------------


def test_sensor_logging(n_iter, log_path):
    """
    test_sensor_logging(n_iter) logs sensor measurement for n_iter
    at log_path in JSON form
    """
    time_dict = {}

    for _iter in range(n_iter):
        # get time
        now = datetime.datetime.now()
        # add second and microsecond
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")

        actions = []
        for _ in range(N_SENSORS):
            sensor_action = random.randint(0, 100)
            actions.append(sensor_action)

        sensors = ["temperature", "humidity", "soil_moisture", "Light"]
        combined_list = list(zip(sensors, actions))
        combined_dict = {key[0]: key[1] for key in combined_list}

        time_dict[current_time] = combined_dict

    log.log(log_path, time_dict, log.MAX_SIZE)


# -------------- VERY BASIC TESTS ------------------


def basic_temp_humid_test(n_iter):
    """
    basic_temp_humid_test(n_iter) runs basic test on temp humid sensor to make sure
    hardware reads properlu
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_si7021.SI7021(i2c)

    for _ in range(n_iter):
        print("\nTemperature: %0.1f C" % sensor.temperature)
        print("Humidity: %0.1f %%" % sensor.relative_humidity)
        time.sleep(2)

    i2c.deinit()


def basic_light_test(n_iter):
    """
    basic_light_test(n_iter) runs basic test on light sensor to make sure
    hardware reads properlu
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_veml7700.VEML7700(i2c)

    for _ in range(n_iter):
        print("Ambient Light: %0.1f " % sensor.light)
        time.sleep(2)

    i2c.deinit()


def basic_moisture_test(n_iter):
    """
    basic_moisture_test(n_iter) runs basic test on moisture sensor to make sure
    hardware reads properlu
    """
    sensor = MCP3001()

    for _ in range(n_iter):
        print("Moisture Level: %f " % sensor.value)
        time.sleep(2)


def three_sensor_test(n_iter):
    """
    three_sensor_test(n_iter) runs basic test on all three sensors to make sure
    hardware reads properlu
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    temp_humid = adafruit_si7021.SI7021(i2c)
    light = adafruit_veml7700.VEML7700(i2c)
    moisture = MCP3001()

    for _ in range(n_iter):
        print("\nTemperature: %0.1f C" % temp_humid.temperature)
        print("Humidity: %0.1f %%" % temp_humid.relative_humidity)

        print("Ambient Light: %0.1f " % light.light)

        print("Moisture Level: %f " % moisture.value)

        time.sleep(2)

    i2c.deinit()


# ---------- MAIN TESTING --------------------
if __name__ == "__main__":
    if RUN_TEST:
        basic_temp_humid_test(N_ITER)
        basic_light_test(N_ITER)
        basic_moisture_test(N_ITER)

        three_sensor_test(N_ITER * 10)

        run_debug(SENSOR_LOG_TEST, N_ITER * 10)
