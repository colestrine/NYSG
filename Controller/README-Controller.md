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
- I2C C

## Sensor Classes (sensor_class.py)

### Description

The sensor class represents a sensor abstraction, that can turn on and off a sensor
and read from the sensor. The Sensor object is meant to be compatiable with I2C.

There are also utility functions, summary functions and debugging functions in sensor_class.py

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
- shut_down : Shuts down the sensor
  
### Sublasses

There are four subclasses. They are all subclasses of Sensor, and have the same
attributes. 
1. Light Sensor
   1. Extra Attributes
      1. Channel - this is the smbus channel object for the I2C channel
      2. Block Size - this is the block size of data in bytes to retrieve from the register

2. Humidity Sensor
   1. Extra Attributes
      1. Channel - this is the smbus channel object for the I2C channel
      2. Block Size - this is the block size of data in bytes to retrieve from the reg
3. Temperature Sensor
   1. Extra Attributes
      1. Channel - this is the smbus channel object for the I2C channel
      2. Block Size - this is the block size of data in bytes to retrieve from the reg
4. Soil Moisture Sensor
   1. Includes sensor attribute, holding an adafruit sensor object
5. C02 Sensor [Optiona]
   1. Includes sensor attribute, holding an adafruit sensor object

### Utility Functions
1. Create Channel - this creates a SMBUS i2C channel . The chnnale must be 1.

### SUMMaRY FUNCTIONS
1. collect_all_sensors() : this returns all the sensor data from the sensors as a fictionary
   in the format {"temperature" : t, "humidity" : h, "soil_moisture" : m, "sunlight" : s}

### DEBUGGING FUNCTIONS
1. Run_debug runs a sensor and logs the data for that sensor
2. run_adafruit_debug runs debugging for a adafruit senxor and logs data for that sensor
3. read_debug_data prints out debug data to screen. Must be run only after a debug function was run first to collect data

## Peripheral Classes (peripheral_class.py)

### Description

The peripheral class represents a peripheral abstraction, that can turn on and off a sensor
and changed at the peripheral. The peripheral object is meant to be compatiable with GPIO pins.

There are also utility functions and debugging functions in peripheral_class.py


### Dependencies

- RPi.GPIO, for GPIO pins communication [Requires a Raspberry Pi for this package]
- Other backup packages
  - gpiozero provides more complex abstractions that may prove fruitful should we need them

### Attributes

1. channel - this represents the GPIO pin channel
2. activity - this represents whether the pin channel is active

### Methods

- setup: Setsup pin channel
- set_active: makes channel active
- set_inactive: makes channe; inactive
- respond: outputs to GPIO channel; device
- read: reads from GPIO channe;
- deactivate: deactives and closes GPIO channel, cleaning up any remnants of chnnael and activity

### Sublasses

There are four subclasses. They are all subclasses of Peripheral, and have the same base
attributes. 
1. Heater
2. Plant Light
3. Water valve
4. Fan
   1. Extra Attributes
      1. PWM attributes
         1. Frequency -current frequency of fan
         2. Duty cycles 0 current duty cycles of fan
         3. PWM  - PWM abstraction for Fan
         4. tach - the tachometer port number
   2. Extra methods
       1. set_freq sets frequnecy
       2. get_freq gets curret frequnccy
       3. Set_dc sets duty cycles
       4. get_dc gets current duty cycles
       5. read_tach - this reads from tachometer, cleans up response and returns estimated RPM



### Summary Functions
1. react_all - this reacts to all the peripherals, changing them the way requested

### DEBUGGING FUNCTIONS
1. debug_peripheral runs a peripheral and logs the data for that peripheral
2. debug_fan runs debugging for a fan, changes duty cycles and logs the recorded tachometer speed
3. read_debug_data prints out debug data to screen. Must be run only after a debug function was run first to collect data 

## Main (main.py)
Main houses all driver program functions. This is where the function is executed from. 
Running main will start up the initialization and the event loop to continuosly monitor sensor data and also change peripeherals. The machine learning algorithm ties into the system in main.

### Dependencies:
pin_constants - these are the constants used
sensor_class - sensors imported
peripheral class - peripherals imported

### ML Wrapper
1. ml_adapter: the ml function is called from here, and argument dictionaries are used to feed in and pipe out data to this adapter

### INTIALIZATION
1. init: sets up controller with sensors and peripherasl and the associated channels and reigsters and pins

### EVENT LOOP DRIVER

1. one_cycle_sensors: polls data from all sensors once
2. one_cycle_peripherals sends voltages to all peripherals once
3. event_loop: measures data from sensor, makes deicsion, logs data and sends out decision to change peripherals, waits a time amount and restarts cycle


### ASYNCHRONICITY

The program is not asynchronous at the present moment. If we have difficulties, weith certain areas we can make sure that the program becomes asynchronous. 


### Debugging

TODO in future

## Log (log.py)
Log contains all the logging utilities and functions to help log data in json files

- get_file_size is the size of the file in bytes
- append_dict adds on to the dict keys that are assumed not to be in the dict
- merge_dict is a utility methodn that ios much slower and adds keys uniquely
- log logs the data, either overwriting prior memory location if the file size is to large or appending data if necessary

## Alert (alert.py)
Alert contains all the alert utilities to monitor, raise and log alerts for the user

- alert is the collection of alerts raised

## Pin Constants (pin_constants.py)
Pin constants contains pin information like GPIO pins, register number, channel numbers and I2C commands.

## run_greenhouse.sh
Runs the greenhouse by calling main


## Set up to Run
To Run this program, run the command
```{bash}
bash run_greenhouse.sh
```
The program will start immediately and will not terminate.

Right now, there is a provision to run the scriot every 10 seconds automatically by bash. The shell will handle all concurrency issues so that we can run other programs.

If you run using the second command, you will be able to run other programs as well. For example, this could allow us to run manage.py to allow the Django context to open up a new webpage server, for user interaction.