import gpiozero
import smbus2
import pin_constants


class Sensor:
    def __init__(self):
        pass
# https://gpiozero.readthedocs.io/en/stable/api_spi.html
# use spi devices


class LightSensor(Sensor):
    # we can use https://gpiozero.readthedocs.io/en/stable/api_input.html
    # 13 .1.4 light sensor
    def activate(self):
        pass

    def deactivate(self):
        pass


class HumiditySensor(Sensor):
    pass


class TemperatureSensor(Sensor):
    pass


class MoistureSensor(Sensor):
    pass


def read_from_sensors(bus):
    for sensor_addr in pin_constants.SENSOR_ADDRS:
        bus.read_i2c_block_data(sensor_addr, 0x00, 100)


if __name__ == "__main__":
    channel = 1
    address = 0x60
    reg_write_dac = 0x40
    bus = smbus2.SMBus(channel)
