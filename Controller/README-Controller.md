# NYSG 2020

This is the main controller for the greenhouse. It is responsible for initializing
the software required, and running a main loop by reading sensor data, using the ML
algorithm to decide on a decision, logging the data and decision and then responding
to the decision by changing the peripherals.

## Setup

In order to use the controller and run any associated code, you must setup the 
environment and dependencies. Below, we list two options for setup. 

### Option 1: on normal environment

### Option 2: with venv (not recommended)



## Controller

### Physical Specifications

- Raspberry Pi 4
- 40 GPIO pins
- Power for Raspberry Pi
- WIFI connection on Raspberry Pi 4

### Software Runtime Requirements

Please activate the I2C capabilities on the Raspberry Pi 4 Controller

### Software Dependency Requirements

- smbus2
- RPi.GPIO

To install these dependencies, first install pip on your Raspberry Pi.
Next, run these commands:
```{bash}
    pip install smbus2
```
and 
```{bash}
    pip install RPi.GPIO
```

After installing these packages, next run this command:
```{bash}
    pip install -r requirements.txt
```
This will install all requisite requirements that the controller requires.

## Sensor Classes

### Description

The sensor class represents a sensor abstraction, that can turn on and off a sensor
and read from the sensor. The Sensor object is meant to be compatiable with I2C

### Sensors
There are 3 physical sensors:
1. Light Sensor
2. Temperature & Humidity Sensor
3. Soil Moisture Sensor

There are 4 sensor abstractions (4 classes):
1. Light Sensor
2. Temperature Sensor
3. Humidity Sensor
4. Soil Moisture Sensor


### Dependencies

- smbus2, for I2C communication

### Attributes

1. addr - this represents the I2C address for the sensor
2. register - this represents the register holding data relevant to the sensor

### Methods

- read: This reads the requested value(s) from the sensor and returns the value

### Sublasses

There are four subclasses. They are all subclasses of Sensor, and have the same
attributes. 
1. Light Sensor
2. Humidity and Temperature Sensor
3. Soil Moisture Sensor
   1. Includes sensor attribute, holding an adafruit sensor object
4. C02 Sensor [Optiona]
   1. Includes sensor attribute, holding an adafruit sensor object

## Peripheral Classes

### Description

The peripheral class represents a peripheral abstraction, that can turn on and off a sensor
and changed at the peripheral. The peripheral object is meant to be compatiable with GPIO pins.

### Dependencies

- RPi.GPIO, for GPIO pins communication
- Other backup packes

### Attributes

1. channel - this represents the GPIO pin channel
2. register - this represents the register holding data relevant to the sensor

### Methods

- read: This reads the requested value(s) from the sensor and returns the value

### Sublasses

There are four subclasses. They are all subclasses of Peripheral, and have the same base
attributes. 
1. Heater
2. Plant Light
3. Water valve
4. Fan
   1. Includes PWM capability, and thus requires a duty cycles and frequency attribute
