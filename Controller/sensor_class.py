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
"""


import smbus2
import time
import json
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

    RELATED:
    # we can use https://gpiozero.readthedocs.io/en/stable/api_input.html
    # 13 .1.4 light sensor
    """

    def __init__(self, addr, register):
        """
         __init__(self, addr, register) is the LightSensor object representing
        a physical light sensor
        """
        super().__init__()
        self.addr = addr
        self.register = register

    def read(self, bus):
        """
        reads the light value from the Light sensor on [bus]
        """
        return bus.read_i2c_block_data(self.addr, self.register, 1)


class TempHumiditySensor(Sensor):
    """
    TemperatureSensor represents a Temperature Sensor and a Humidity Sensor

    SUPERCLASS: Sensor

    [addr] is the I2C address for the physical TemperatureHUmidity Sensor
    [register] is the address for the register with the data in the physical sensor
    [block_size] is the size of the data retrieved from a read, requieres 2
    """

    def __init__(self,  addr, register, block_size=2):
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
        self.block_size = block_size

    def read(self, bus):
        """
        read(self, bus) reads the temperature from the physical temperature sensor and returns
        the temperature in Celsius

        [bus] is a bus object representing the I2C bus to which the temperature
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
            bus.read_i2c_block_data(
                self.addr, self.register, self.block_size))


class MoistureSensor(Sensor):
    """
    MoistureSensor represents an AdaFruit Moisture Sensor
    """

    def __init__(self):
        super().__init__()


def read_from_sensors(bus):
    for sensor_addr in pin_constants.SENSOR_ADDRS:
        bus.read_i2c_block_data(sensor_addr, 0x00, 100)


def create_channel(bus_num=1):
    """
    create_channel(bus_num) creates a channel for I2C communication
    on bus_num bus number.

    SUGGEST: bus_num as 1 or 0

    WRAPPER FUNCTION for students
    """
    return smbus2.SMBus(bus_num)

# --------- LOGGING -------------


def load_data(path):
    fp = open(path, "r")
    obj = json.load(fp)
    fp.close()
    return obj


def dump_data(obj, path):
    fp = open(path, "w")
    json.dump(obj, fp)
    fp.close()


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


if __name__ == "__main__":
    pass
