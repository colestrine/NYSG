"""
sensor_class includes information relating to the sensors
for the greenhourse:
    - LightSensor
    - HumiditySensor
    - MoistureSensor
    - TemperatureSensor
    - [optiona] CO2Sensor

High level classes to abstract away complications are given
to the students to use.


PACKAGE REQUIREMENTS:
- smbus2 (used to create channels for I2C and for reading and writing using
I2C protocols)
- time (used for time and delays)
- json (used to log read in data from sensors)
- pin_constants [custom]: holds pin data for I2C communication protocols
TODO: REQUIRE SPIDEV TODO:

- sudo pip3 install adafruit-circuitpython-seesaw
 You will need to run the above command for the adafruit moisture sensor
 to work

- sudo pip3 install adafruit-circuitpython-sgp30
You will need to run the above command to access and work with the adafruit
co2 sensor

NOTE: None of the Adafruit products contain a register so they cannot be accessed
easily, without using their cusotm packages
TODO: CHECK AND TEST ALL CLASSES
"""

# ----- ADA FRUIT SENSOR IMPORTS -----------------
import busio
import board

from adafruit_seesaw.seesaw import Seesaw
import Adafruit_PureIO
import adafruit_si7021
import adafruit_veml7700

# Adafruit_I2C import Adafruit_I2C

# ---- ADA FRUIT IMPORTS CO2 GAS SENSOR IMPORTS----------
import adafruit_sgp30

# ----- NON ADA FRUIT IMPORTS ------

import smbus2
from gpiozero import MCP3001
# https://buildmedia.readthedocs.org/media/pdf/smbus2/latest/smbus2.pdf
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/legacy/Adafruit_I2C/Adafruit_I2C.py
# https://github.com/adafruit/Adafruit_Python_PureIO/blob/master/Adafruit_PureIO/smbus.py


# ------- OTHER IMPORTS -------
import time
from datetime import datetime
import pin_constants


# -------- TEST IMPORTS ----------
import random
import datetime
import sys
import log


# ------- TEST CONSTANTS ----------
N_SENSORS = 4
N_ITER = 100
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


SCL = 1
SDA = 1

# --------- SENSORS ----------------


class Sensor:
    """
    Sensor is represents an abstract Sensor

    Sensor is an ABSTRACT class
    INCLUDES: abstract method
        - read: to read from a sensor
    SUBCLASSES:
        - LightSensor
        - HumiditySensor
        - TemperatureSensor
        = MoistureSensor
        - [opt] CO2Sensor
    DO NOT INSTANTIATE

    ----- ADDITIONAL SOURCES -------
    # https://gpiozero.readthedocs.io/en/stable/api_spi.html
    # use spi devices
    """

    def __init__(self):
        pass

    def read(self):
        pass

    def shut_down(self):
        pass


class LightSensor(Sensor):
    """
    LightSensor represents a Light Sensor from VISHAY ELECTRONICS

    SUPERCLASS: SENSOR

    pip3 install adafruit-circuitpython-veml7700

    [addr] is the I2C address of the sensor in the bus
    [register] is the sensor data location
    [channel] is the channel for the sensor
    [block_size] is the block siz eofk the data from the I2C compatible sensor

    RELATED:
    # we can use https://gpiozero.readthedocs.io/en/stable/api_input.html
    # 13 .1.4 light sensor
    """

    # def __init__(self, addr, register, channel, block_size=1):
    #     """
    #      __init__(self, addr, register) is the LightSensor object representing
    #     a physical light sensor
    #     """
    #     super().__init__()
    #     self.addr = addr
    #     self.register = register
    #     self.channel = channel
    #     self.block_size = block_size

    #     self.channel.open(pin_constants.I2C_PORT_NUM)

    # def read(self):
    #     """
    #     reads the light value from the Light sensor on self.channel
    #     """

    #     def convert_light(light):
    #         # take LSB 8 buts
    #         return light & (2 ** 8)

    #     light = self.channel.read_i2c_block_data(self.addr, self.register, 2)
    #     return convert_light(light)

    # def shut_down(self):
    #     self.channel.close()

    def __init__(self, i2c_channel):
        self.channel = i2c_channel
        sensor = adafruit_veml7700.VEML7700(i2c_channel)
        self.sensor = sensor

    def read_light(self):
        """
        read_light(sensor) is the ambient light from the sensor
        """
        return self.sensor.light


class TempHumiditySensor(Sensor):
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


class HumiditySensor(Sensor):
    """
    TemperatureSensor represents a Temperature Sensor and a Humidity Sensor

    SUPERCLASS: Sensor

    [addr] is the I2C address for the physical TemperatureHUmidity Sensor
    [register] is the address for the register with the data in the physical sensor
    [block_size] is the size of the data retrieved from a read, requieres 2
    [channel] is the I2C channel
    """

    def __init__(self,  addr, register, channel, block_size=2):
        """
        __init__(self, bus, addr, register, block_size) creates a Temperature Sensor
        object on bus object [bus], I2C address for the physical temperature sensor [addr],
        [register] number register on the physical temperature sensor and
        [block_size] number of bytes of data retrieved every time data is read
        from the physical temperature sensor
        """
        super().__init__()
        self.addr = addr
        self.register = register
        self.channel = channel
        self.block_size = block_size

        self.channel.open(pin_constants.I2C_PORT_NUM)

    def read(self):
        """
        read(self, bus) reads the temperature from the physical temperature sensor and returns
        the temperature in Celsius

        self.channel is a bus object representing the I2C bus to which the temperature
        and humidity sensor is connected to

        Returns: Float (Celsius Temperature)

        SOURCE ATTRIBUTION for twos_comp and convert_temp
        # https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-4-i2c-temperature-sensor
        """
        def convert_humidity(sensor_humidity_code):
            return 125 * sensor_humidity_code / 65536 - 6

        def truncate_humidity(rh):
            if rh > 100:
                return 100
            if rh < 0:
                return 0
            return rh

        # do the write to the device to do a no hold temp measure
        self.channel.write_byte(
            self.addr, pin_constants.MEASURE_RH_REGISTER_NO_HOLD)
        humidity_code = self.channel.read_i2c_block_data(
            self.addr, self.register, self.block_size)
        rh = truncate_humidity(convert_humidity(humidity_code))

        return rh

    def shut_down(self):
        self.channel.close()


class TemperatureSensor(Sensor):
    """
    TemperatureSensor represents a Temperature Sensor and a Humidity Sensor

    SUPERCLASS: Sensor

    [addr] is the I2C address for the physical TemperatureHUmidity Sensor
    [register] is the address for the register with the data in the physical sensor
    [block_size] is the size of the data retrieved from a read, requieres 2
    [channel] is the I2C channel
    """

    def __init__(self,  addr, register, channel, block_size=2):
        """
        __init__(self, bus, addr, register, block_size) creates a Temperature Sensor
        object on bus object [bus], I2C address for the physical temperature sensor [addr],
        [register] number register on the physical temperature sensor and
        [block_size] number of bytes of data retrieved every time data is read
        from the physical temperature sensor
        """
        super().__init__()
        self.addr = addr
        self.register = register
        self.channel = channel
        self.block_size = block_size

        self.channel.open(pin_constants.I2C_PORT_NUM)

    def read(self):
        """
        read(self, bus) reads the temperature from the physical temperature sensor and returns
        the temperature in Celsius

        self.channel is a bus object representing the I2C bus to which the temperature
        and humidity sensor is connected to

        Returns: Float (Celsius Temperature)

        SOURCE ATTRIBUTION for twos_comp and convert_temp
        # https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-4-i2c-temperature-sensor
        """

        def convert_temp(temp_code):
            return 175.72 * temp_code / 65536 - 46.85

        def c_to_f(c):
            return 9/5 * c + 32

        # do the write to the device to do a no hold temp measure
        self.channel.write_byte(
            self.addr, pin_constants.MEASURE_TEMP_REGISTER_NO_HOLD)
        temp_code = self.channel.read_i2c_block_data(
            self.addr, self.register, self.block_size)
        temp = c_to_f(convert_temp(temp_code))

        return temp

    def shut_down(self):
        self.channel.close()


class MoistureSensor(Sensor):
    """
    MoistureSensor represents an AdaFruit Moisture Sensor

    [sensor] is the sensor object for Adafruit

    WARNING!  - if you have a non-express board, you must install the following
    packages from dadafruit
    adafruit_seesaw.mpy
    adafruit_bus_device
    Adafruit_Blinka

    Before continuing make sure your board's lib folder or root filesystem has
    the adafruit_seesaw.mpy, and adafruit_bus_device files and folders copied over

    SOURCE ATTRIBUTION:
    https://www.mouser.com/pdfdocs/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor.pdf
    """

    # def __init__(self):
    #     """
    #     Creates a Moisture sensor represent an adaFruit Moisture Sensor
    #     """
    #     super().__init__()
    #     i2c_bus = busio.I2C(SCL, SDA)
    #     ss = Seesaw(i2c_bus, addr=pin_constants.MOISTURE_ADDR)
    #     self.sensor = ss

    #     # need to add try and except to locka nd unlcok judiviously
    #     # channel = Adafruit_PureIO.smbus.SMBus(bus=pin_constants.I2C_PORT_NUM)

    # def read(self):
    #     """
    #     read(self) returns the moisture and the soil_temp for the given
    #     Moisture sensor
    #     """
    #     ss = self.sensor
    #     # read moisture level through capacitive touch pad
    #     moisture = ss.moisture_read()
    #     # read temperature from the temperature sensor
    #     soil_temp = ss.get_temp()
    #     _ = soil_temp  # ignore
    #     return moisture

    # def shut_down(self):
    #     pass

    def __init__(self):
        self.sensor = MCP3001(channel=0)

    def read_moisture(self):
        """
        read_moisture(self) is the moisture read
        """
        return self.sensor.value


class Co2Sensor(Sensor):
    """
    Co2Sensor represents a physical Ada Fruit Co2 Sensor

    SUPERCLASS: Sensor
    [OPTIONAL] for use
    """

    def __init__(self):
        i2c = busio.I2C(SCL, SDA, frequency=100000)
        # Create library object on our I2C port
        sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        sgp30.iaq_init()
        sgp30.set_iaq_baseline(0x8973, 0x8aae)
        self.sensor = sgp30

    def read(self):
        return self.sensor.iaq_measure()

    def shut_down(self):
        pass

# -------- UTILITIES ------------


def create_channel(bus_num=1):
    """
    create_channel(bus_num) creates a channel for I2C communication
    on bus_num bus number.

    SUGGEST: bus_num as 1 or 0

    WRAPPER FUNCTION for students
    """
    return smbus2.SMBus(bus_num)


# -------- SUMMARY FUNCTIONS --------


def sensor_to_name(sensor):
    """
    sensor_to_name(sensor) converts the type of the sensor to a name
    """
    if type(sensor) == Co2Sensor:
        return "CO2"
    elif type(sensor) == TemperatureSensor:
        return "temperature"
    elif type(sensor) == HumiditySensor:
        return "humidity"
    elif type(sensor) == MoistureSensor:
        return "soil_moisture"
    elif type(sensor) == LightSensor:
        return "sunlight"
    else:
        raise AssertionError


def collect_all_sensors(sensor_list):
    """
    collect_all() collects all the data from all sensors and logs it
    uses the sensors in [sensor_list] which are on the bus object sensor.channel

    Returns the logged data
    """
    ret_dict = {}

    for sensor in sensor_list:
        if hasattr(sensor, "sensor"):
            s = sensor.sensor
            val = s.read()
        else:
            val = sensor.read(sensor.channel)

        name = sensor_to_name(sensor)

        ret_dict[name] = val

    # get time
    now = datetime.datetime.now()
    # add second and microsecond
    current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")

    outer_dict = {}
    outer_dict[current_time] = ret_dict
    return outer_dict


# -------- DEBUGGING ------------


def run_debug(log_path, addr, register, cycles):
    """
    run_debug() is used to create a sample bus channel and read from the channel

    logs data in pin_constants.TEMPERATURE_LOG_PATH as a json dictionary
    mapping the current time as a string to the temperature recorded

    REQUIRES: pin_constants.TEMPERATURE_LOG_PATH contains a dictionary of the
    the data, could be empty
    RECORDS for [cyclkes]number of iteractions
    """
    channel = pin_constants.I2C_PORT_NUM
    bus = smbus2.SMBus(channel)

    log_dict = pin_constants.load_data(log_path)
    i = 0
    while i < cycles:
        val = bus.read_i2c_block_data(addr, register, 2)
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M")
        log_dict[current_time] == val
        i += 1

    pin_constants.dump_data(log_dict, log_path)


def run_adafruit_debug(log_path, addr, register, cycles):
    """
    run_adafruit_debug() is used to create a sample bus channel and read from the channel
    for the adafruit moisture sensor

    logs data in pin_constants.TEMPERATURE_LOG_PATH as a json dictionary
    mapping the current time as a string to the temperature recorded

    REQUIRES: pin_constants.TEMPERATURE_LOG_PATH contains a dictionary of the
    the data, could be empty
    RECORDS for [cyclkes]number of iteractions
    """
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=addr)

    temp_log_dict = pin_constants.load_data(log_path)
    i = 0
    while i < cycles:
        val = ss.moisture_read()
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M")
        temp_log_dict[current_time] == val
        i += 1

    pin_constants.dump_data(temp_log_dict, pin_constants.TEMPERATURE_LOG_PATH)


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


# ---------- TEST SENSOR LOGGING -------------
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


# -------------- BASIC TESTS ------------------
def basic_temp_humid_test(n_iter):
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_si7021.SI7021(i2c)

    for _ in range(n_iter):
        print("\nTemperature: %0.1f C" % sensor.temperature)
        print("Humidity: %0.1f %%" % sensor.relative_humidity)
        time.sleep(2)


def basic_light_test(n_iter):
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_veml7700.VEML7700(i2c)

    for _ in range(n_iter):
        print("\Ambient Light: %0.1f " % sensor.light)
        time.sleep(2)


def basic_moisture_test(n_iter):
    sensor = MCP3001(channel=0)

    for _ in range(n_iter):
        print("\Moisture Level: %0.1f " % sensor.value)
        time.sleep(2)
    # print("Creating Channel")
    # channel = create_channel(pin_constants.I2C_PORT_NUM)
    # print("Opening Channel on port # : " + str(pin_constants.I2C_PORT_NUM))
    # channel.open(pin_constants.I2C_PORT_NUM)
    # print("Writing read command on Channel on port # : " +
    #       str(pin_constants.I2C_PORT_NUM))
    # print("Command is to measure temperatuee no hold : " +
    #       str(pin_constants.MEASURE_TEMP_REGISTER_NO_HOLD))
    # channel.write_byte(
    #     pin_constants.TEMP_ADDR, pin_constants.MEASURE_TEMP_REGISTER_NO_HOLD)
    # print("Reading temperature (2 bytes) with command : " +
    #       str(pin_constants.READ_TEMP_HUMID))
    # temp_code = channel.read_i2c_block_data(
    #     pin_constants.TEMP_ADDR, pin_constants.READ_TEMP_HUMID, 2)
    # print(temp_code)
    # print("Closing Channel")
    # channel.close()


# ---------- MAIN TESTING --------------------
if __name__ == "__main__":
    # if RUN_TEST:
    #     log.init_log(SENSOR_LOG_TEST)
    #     test_sensor_logging(N_ITER, SENSOR_LOG_TEST)
    N_ITER = 4
    basic_temp_humid_test(N_ITER)
    basic_light_test(N_ITER)
    basic_moisture_test(N_ITER)
