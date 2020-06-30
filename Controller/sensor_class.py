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

    RELATED:
    # we can use https://gpiozero.readthedocs.io/en/stable/api_input.html
    # 13 .1.4 light sensor
    """

    def __init__(self, addr, register, channel):
        """
         __init__(self, addr, register) is the LightSensor object representing
        a physical light sensor
        """
        super().__init__()
        self.addr = addr
        self.register = register
        self.channel = channel

    def read(self):
        """
        reads the light value from the Light sensor on self.channel
        """
        return self.channel.read_i2c_block_data(self.addr, self.register, 1)


class TempHumiditySensor(Sensor):
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
        def twos_comp(val, bits):
            if (val & (1 << (bits - 1))) != 0:
                val = val - (1 << bits)
            return val

        def convert_temp(raw_temp):
            temp_cel = (raw_temp[0] << 4) | (raw_temp[1] >> 4)
            temp_cel = twos_comp(temp_cel, 12)
            temp_cel = temp_cel * 0.0625
            return temp_cel

        return convert_temp(
            self.channel.read_i2c_block_data(
                self.addr, self.register, self.block_size))


class MoistureSensor(Sensor):
    """
    MoistureSensor represents an AdaFruit Moisture Sensor

    [sensor] is the sensor object for Adafruit

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
        return (moisture, soil_temp)


class Co2Sensor(Sensor):
    """
    Co2Sensor represents a physical Ada Fruit Co2 Sensor

    SUPERCLASS: Sensor
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
    elif type(sensor) == TempHumiditySensor:
        return "Temp_Humidity"
    elif type(sensor) == MoistureSensor:
        return "Moisture"
    elif type(sensor) == LightSensor:
        return "Light"
    else:
        raise AssertionError


def collect_all_sensors(sensor_list, log_path=None, log=False):
    """
    collect_all() collects all the data from all sensors and logs it
    uses the sensors in [sensor_list] which are on the bus object sensor.channel

    logs data if log = True
    log_dict is the place to log data

    Returns the logged data
    """
    ret_dict = {}

    log_dict = pin_constants.load_data(log_path)

    for sensor in sensor_list:
        if hasattr(sensor, "sensor"):
            s = sensor.sensor
            val = s.read()
        else:
            val = sensor.read(sensor.channel)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        name = sensor_to_name(sensor)

        ret_dict[name] = val

        if log:
            log_dict[name][current_time] == val

    if log:
        pin_constants.dump_data(log_dict, log_path)

    return ret_dict


# -------- DEBUGGING ------------


def run_debug():
    """
    run_debug() is used to create a sample bus channel and read from the channel

    logs data in pin_constants.TEMPERATURE_LOG_PATH as a json dictionary
    mapping the current time as a string to the temperature recorded

    REQUIRES: pin_constants.TEMPERATURE_LOG_PATH contains a dictionary of the
    the data, could be empty
    """
    channel = pin_constants.I2C_PORT_NUM
    bus = smbus2.SMBus(channel)

    address = pin_constants.TEMP_ADDR
    register = pin_constants.TEMP_REGISTER

    temp_log_dict = load_data(pin_constants.TEMPERATURE_LOG_PATH)
    i = 0
    while i < 1000:
        val = bus.read_i2c_block_data(address, register, 2)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        temp_log_dict[current_time] == val

        i += 1
    dump_data(temp_log_dict, pin_constants.TEMPERATURE_LOG_PATH)
