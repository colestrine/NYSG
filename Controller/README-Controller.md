# NYSG 2020

This is the main controller for the greenhouse. It is responsible for initializing
the software required, and running a main loop by reading sensor data, using the ML
algorithm to decide on a decision, logging the data and decision and then responding
to the decision by changing the peripherals.

## Setup

In order to use the controller and run any associated code, you must setup the 
environment and dependencies. 

### Software Runtime Requirements

Please activate the I2C capabilities on the Raspberry Pi 4 Controller. To do so
follow these instructions:

(these instructions are from: https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/#:~:text=Method%201%20%E2%80%93%20Using%20%E2%80%9CRaspi%2Dconfig%E2%80%9D%20on%20Command%20Line&text=Highlight%20the%20%E2%80%9CI2C%E2%80%9D%20option%20and,activate%20%E2%80%9C%E2%80%9D.&text=The%20Raspberry%20Pi%20will%20reboot%20and%20the%20interface%20will%20be%20enabled.)

#### Method 1: Command Line

1. Open a new terminal tab
2. Run 
```{bash}
    sudo raspi-config
```
3. Select "Interfacing Options"
4. Scroll to the I2C option and activate by selecting <YES>
5. Click "<ok>" to activate ARM I2C interface 
6. Click "<Yes>" to reboot

#### Method 2: User Interface
1. On Desktop go to 
   Menu > Preferences > Raspberry Pi Configuration
2. Select "Interfaces" and set "I2C" to "Enabled"
3. Click "OK"
4. Click "Yes" to reboot


Next, you will need to install smbus and I2C tools. 
To do so, run the following commands on a terminal tab
1. Open a terminal tab
2. Run
```{bash}
    sudo apt-get update
    sudo apt-get install -y python-smbus i2c-tools
```
To install I2C hardware, start by shutting down the Raspberry Pi.
Run:
```{bash}
    sudo halt
```
Wait 10 seconds, disconnect PI power, and connect hardware. 


To check if I2C enabled, power up the PI.
Run:
```{bash}
    lsmod | grep i2c_
```
If “i2c_bcm2708” is listed, i2c is working. 

To check hardware is working:
run this command:
```{bash}
    i2cdetect -y 1
```

You should get a grid of numbers, with the numbers filled in being the i2c addresses.
Note that you need a newer Raspberry Pi model for the last command.

### Software Dependency Requirements

Two packages are crucial for Raspberry Pi software for the controller.
- smbus2
- RPi.GPIO

To install these dependencies, first install pip on your Raspberry Pi.
If pip is installed, run
```{bash}
     pip --version 
```

Also run:
```{bash}
     python3 --version
```
You'll a version of python3 greater or equal to Python 3.7.6

Next run this command:
```{bash}
    pip install -r requirements.txt
```
This will install all requisite requirements that the controller requires.

## Controller

### Physical Specifications

- Raspberry Pi 4
- 40 GPIO pins
- Power for Raspberry Pi
- WIFI connection on Raspberry Pi 4

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
