# -----I2C constants --------

SDA = 3
SCL = 5

TEMP_ADDR = 0x40
MOISTURE_ADDR = 0x36
LIGHT_ADDR = 0x10
CO2_ADDR = 0x58

TEMP_REGISTER = 0xE7
LIGHT_REGISTER = 0x04

# ---- MODIFY SENSOR ADDRS FOR WHICH SENSORS ARE USED ----
SENSOR_ADDRS = [
    TEMP_ADDR,
    MOISTURE_ADDR,
    LIGHT_ADDR,
    CO2_ADDR,
]

I2C_PORT_NUM = 1

# ----- Peripheral Constants --------

VENT = 33
LED = 37
VALVE = 32
HEAT = 37

# ------- lOG LOCATIONS -------------
TEMPERATURE_LOG_PATH = "temperature_log.json"
