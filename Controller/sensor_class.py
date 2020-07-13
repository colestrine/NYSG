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

# ----- ADA FRUIT MOISTURE SENSOR IMPORTS -----------------
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

# ---- ADA FRUIT IMPORTS CO2 GAS SENSOR IMPORTS----------
import adafruit_sgp30

# ----- NON ADA FRUIT IMPORTS ------

import smbus2

# ------- OTHER IMPORTS -------
import time
from datetime import datetime
import pin_constants

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


class LightSensor(Sensor):
    """
    LightSensor represents a Light Sensor from VISHAY ELECTRONICS

    SUPERCLASS: SENSOR

    [addr] is the I2C address of the sensor in the bus
    [register] is the sensor data location
    [channel] is the channel for the sensor
    [block_size] is the block siz eofk the data from the I2C compatible sensor

    RELATED:
    # we can use https://gpiozero.readthedocs.io/en/stable/api_input.html
    # 13 .1.4 light sensor
    """

    def __init__(self, addr, register, channel, block_size=1):
        """
         __init__(self, addr, register) is the LightSensor object representing
        a physical light sensor
        """
        super().__init__()
        self.addr = addr
        self.register = register
        self.channel = channel
        self.block_size = block_size

    def read(self):
        """
        reads the light value from the Light sensor on self.channel
        """

        def convert_light(light):
            # take LSB 8 buts
            return light & (2 ** 8)

        light = self.channel.read_i2c_block_data(self.addr, self.register, 2)
        return convert_light(light)


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

    def __init__(self):
        """
        Creates a Moisture sensor represent an adaFruit Moisture Sensor
        """
        super().__init__()
        i2c_bus = busio.I2C(SCL, SDA)
        ss = Seesaw(i2c_bus, addr=pin_constants.MOISTURE_ADDR)
        self.sensor = ss

    def read(self):
        """
        read(self) returns the moisture and the soil_temp for the given
        Moisture sensor
        """
        ss = self.sensor
        # read moisture level through capacitive touch pad
        moisture = ss.moisture_read()
        # read temperature from the temperature sensor
        soil_temp = ss.get_temp()
        _ = soil_temp  # ignore
        return moisture


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

    time = datetime.strftime()

    outer_dict = {}
    outer_dict[time] = ret_dict
    return outer_dict


# -------- DEBUGGING ------------


def run_debug_temp():
    """
    run_debug_temp() is used to create a sample bus channel and read from the channel

    logs data in pin_constants.TEMPERATURE_LOG_PATH as a json dictionary
    mapping the current time as a string to the temperature recorded

    REQUIRES: pin_constants.TEMPERATURE_LOG_PATH contains a dictionary of the
    the data, could be empty
    """
    channel = pin_constants.I2C_PORT_NUM
    bus = smbus2.SMBus(channel)

    address = pin_constants.TEMP_ADDR
    register = pin_constants.TEMP_REGISTER

    temp_log_dict = pin_constants.load_data(pin_constants.TEMPERATURE_LOG_PATH)
    i = 0
    while i < 1000:
        val = bus.read_i2c_block_data(address, register, 2)

        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M")

        temp_log_dict[current_time] == val

    i += 1
    pin_constants.dump_data(temp_log_dict, pin_constants.TEMPERATURE_LOG_PATH)
