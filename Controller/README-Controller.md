# NYSG 2020

This is the main controller for the greenhouse. It is responsible for initializing
the software required, and running a main loop by reading sensor data, using the ML
algorithm to decide on a decision; or using manual control to influence the actions, logging the data and decision, sending any alerts as specified by the user and then responding to the decision by changing the peripherals. The controller than pauses until the next cycle of execution.

## Setup

In order to use the controller and run any associated code, you must setup the 
environment and dependencies. 

### Software Runtime Requirements

Please activate the I2C capabilities on the Raspberry Pi 4 Controller. To do so
follow these instructions:

(these instructions are from: https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/#:~:text=Method%201%20%E2%80%93%20Using%20%E2%80%9CRaspi%2Dconfig%E2%80%9D%20on%20Command%20Line&text=Highlight%20the%20%E2%80%9CI2C%E2%80%9D%20option%20and,activate%20%E2%80%9C%E2%80%9D.&text=The%20Raspberry%20Pi%20will%20reboot%20and%20the%20interface%20will%20be%20enabled.)

Please also activate the SPI capabilities on the Raspberry Pi Controller. 
https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

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
7. Then run 
```bash
sudo raspi-config
```
8. Select "Interfacing Options"
9. Scroll to the SPI option and activate by selecting <YES>
5. Click "<ok>" to activate ARM I2C interface 
6. Click "<Yes>" to reboot

#### Method 2: User Interface
1. On Desktop go to 
   Menu > Preferences > Raspberry Pi Configuration
2. Select "Interfaces" and set "I2C" to "Enabled"
3. Click "OK"
4. Click "Yes" to reboot
5. On Desktop go to 
   Menu > Preferences > Raspberry Pi Configuration
2. Select "Interfaces" and set "SPI" to "Enabled"
3. Click "OK"
4. Click "Yes" to reboot


Next, you will need to install smbus, spi and I2C tools. 
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

Also run the two commands
```{bash}
    sudo apt-get install -y python-dev python3-dev
    sudo apt-get install -y python-spidev python3-spidev
```

Then run the following commands:
``` bash
cd ~
git clone https://github.com/Gadgetoid/py-spidev.git
cd py-spidev
sudo python setup.py install
sudo python3 setup.py install
cd ~
```

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
Note that you need a newer Raspberry Pi model for the last command. So i2c should work.

To verify spi:
run 
```bash
lsmod | grep spi_
```
and “spi_bcm2708″ or “spi_bcm2835” should be listed
### I2C clock stretching
1. Open terminal
2. Type "sudo nano /boot/config.txt"
3. Scroll down to where you see the line "dtparam=spi=on" (assuming SPI is on)
4. After that line, add the line "dtparam=i2c_arm_baudrate=10000"
5. Hit ctrl-x and y to save the file.
6. Type "sudo reboot" into terminal to restart the Pi. 
This changes the clock rate for the I2C bus to 10kHz. If this is still too fast, chang 10000 to 5000  

### Software Dependency Requirements


#### Dependencies
Two packages are crucial for Raspberry Pi software for the controller.
- RPi.GPIO
- gpiozero
Several other packages are used jointly in the controller and must also be installed. These include a host of Adafruit custom packages To install, run the commands below.

#### Installation
To install these dependencies, first install pip on your Raspberry Pi. You will need to be on termianl on the command line, type these commands and hit enter afer each for them to take effect. 
If pip3 is installed, run
```{bash}
     pip3 --version 
```
It should show a version number

Also run:
```{bash}
     python3 --version
```
You'll a version of python3 greater or equal to Python 3.7.6

Next run this command:
```{bash}
    pip install -r requirements.txt
```
This will install all requisite requirements that the controller requires, 
including all the necessary packages for the controller. This command will take some time to run since many dependencies must be installed, and started, so be patient.

## Controller

### Physical Specifications

- Raspberry Pi 4 B
- 40 GPIO pins
- Power for Raspberry Pi
- WIFI connection on Raspberry Pi 4
- I2C capability
- SPI capability

## Sensor Classes (sensor_class.py)

### Description

The sensor class represents a sensor abstraction, that can turn on and off a sensor
and read from the sensor. The Sensor object is meant to be compatible with I2C, and GPIOZEROfor the SPI capability.

There are also utility functions, summary functions and debugging functions in sensor_class.py

### Sensors
There are 3 physical sensors:
1. Light Sensor
2. Temperature & Humidity Sensor
3. Soil Moisture Sensor

There are 3 sensor abstractions (4 classes):
1. Light Sensor
2. Temperature and Humidity Sensor
3. Soil Moisture Sensor

### Dependencies

- GPIOZERO, for spi communication, specifically MCP7001 (moisture sensor)
- busio
- board
- Adafruit_PureIO
- adafruit_si7021 (temp humidity sensor_)
- adafruit_veml7700 (light sensor)

### Attributes

1. addr - this represents the I2C address for the sensor
2. register - this represents the register holding data relevant to the sensor

### Methods

- read: This reads the requested value(s) from the sensor and returns the value
- shut_down : Shuts down the sensor
  
### Classes

There are four classes. Attributes and Methods are documented below

1. Light Sensor
   1. Attributes
      1. channel. - this represents the I2C channel number for the sensor
      2. sensor - this represents the adafruit VEML7700 sensor object
   2. Methods
      1. read_light: This reads the requested ambient light value from the sensor and returns the value
2. TempHumidity Sensor
   1. Attributes
      1. channel. - this represents the I2C channel number for the sensor
      2. sensor - this represents the adafruit si7021 sensor object
   2. Methods
      1. read_temp: This reads the requested temperature value from the sensor and returns the value
      2. read_rh: This reads the requested relative humidity value from the sensor and returns the value
3. Soil Moisture Sensor
   1. Attributes
      1. Sensor - this reresents the gpiozero MCP3001 soil moisture object abstraction
   2. Methods
      1. read_moisture: This reads the requested soil moisture value from the sensor and returns the value

### Utility Functions
1. Create Channel - this creates a Adafruit bus i2C channel . The chnnale must be 1.

### SUMMARY FUNCTIONS
1. collect_all_sensors() : this returns all the sensor data from the sensors as a dictionary in the format 
```python
{str_time: {"temperature" : t, "humidity" : h, "soil_moisture" : m, "sunlight" : s}}
```
where str_time is the current time given by strftime in datetime.datetime up to seconds.

### DEBUGGING FUNCTIONS
1. Run_debug runs a sensor and logs the data for that sensor
2. read_debug_data prints out debug data to screen. Must be run only after a debug function was run first to collect data
3. test_sensor_logging tests sensor logging functionality
4. basic_temp_humid_test makes sure the temperature sensor can be read and prints out the values of temeprature
5. basic_light_test makes sure ambient light can be read
6. basic_moisture_test makes sure mooisture can be read
7. three_sensor_test makes sure all three sensors can be read at once and prints out temperature, himdiity, moisture and light values

### Running sensor_class.py
Running
```bash
python3 sensor_class.py
```
will run the final 4 debugging tests above.

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
2. active - this represents whether the pin channel is active or not (on or off)

### Methods

- setup: Setsup pin channel and turns on the board settings to BCM at the first peripheral creation
- set_active: makes channel active and makes the GPIO channel respond with high voltage
- set_inactive: makes channl  inactive, and make sGPIo channel respond with low voltage
- respond: outputs to GPIO channel with correct voltage level to device to activate or deactivate
- read: reads from GPIO channe;
- deactivate: deactives and closes GPIO channel, cleaning up any remnants of chnnael and activity

### Sublasses

There are two abstract subclasses. They are all subclasses of Peripheral, and have the same base attributes.
1. BurstPeripheral
   1. Attributes
      1. Burst_time: the time the peripheral runs before turning off
   2. Methods
      1. set_active sets the periphjeral ctive for burst time seconds and then turns off after
      2. Set_inactive turns off peripheral
      3. get_burst_time gets burst time in seconds
      4. set_burst_time sets burst time for the peripheral in seconds
2. Pwm_Peripheral
   1. Attribtes
      1. freq the frequency in Hertz
      2. dc: the duty cycles in percent
      3. pwm: the pwm object to control pwm
   2. Methods
      1. Set_inacvtive: changes duty_cycle to 0 to turn off
      2. set_freq sets freuqnercy in hetz
      3. get_freq gets frequnecy of the pwm device i  hertz
      4. set_duty_cycle sets duty cycle in %
      5. get_duty_cycle gets duty cycle in %
      6. deactivate turns off all pwm devices completely

There are 4 concrete base classes:
1. PlantLight
   1. Superclass
      1. Pwm_peripheral
2. Fan
   1. Superclass
      1. Pwm_peripjeral
   2. Attributes
      1. set_duty_cycle sets the dutcy cyle inverted by subtracting from 100 and taking absolute value
3. HeatPad
   1. Superclass:
      1. Burst_periperhal
4. SolenoidValve
   1. Superclass:
      1. Burst_periperhal


### Summary Functions
1. react_all - this reacts to all the peripherals, changing them the way requested. Runs asynchrnously to allow for yielding
2. translate_action_to_burst_time translates the action to a burst time from interface files
3. change_peripheral changes the peripheral by activating it
4. manual for manual control

### DEBUGGING FUNCTIONS
1. debug_peripheral runs a peripheral and logs the data for that peripheral
2. debug_fan runs debugging for a fan, changes duty cycles and logs the recorded tachometer speed
3. read_debug_data prints out debug data to screen. Must be run only after a debug function was run first to collect data 
4. fan_turn_on_test turns on fan
5. test_peripheral_logging tests peripheal logging capability
   
Running 
```bash
python3 peripheral_class.py
```
will test the fan, check logging and test all four peripherals

## Main (controller_main.py)
Main houses all driver program functions. This is where the function is executed from. Running main will start up the initialization and the event loop to continuosly monitor sensor data and also change peripeherals. The machine learning algorithm ties into the system in main, as does the manual control.

### Dependencies:
pin_constants - these are the constants used
sensor_class - sensors imported
peripheral class - peripherals imported
reinforcement_learning - the ML algorithm

### ML Wrapper
1. ml_adapter: the ml function is called from here, and argument dictionaries are used to feed in and pipe out data to this adapter

### INTIALIZATION
1. init: sets up controller with sensors and peripherasl and the associated channels and reigsters and pins

### EVENT LOOP DRIVER

1. one_cycle_sensors: polls data from all sensors once
2. one_cycle_driver - Testing verhicle fo runnign only one cycle
3. one_cycle_peripherals sends voltages to all peripherals once
4. event_loop: reads in user interface input, measures data from sensor, makes deicsion, logs data and sends out decision to change peripherals, waits a time amount and restarts cycle
5. ml_adapter calls ml function as an adapter pattern funcrtion
6. process_from_ml processes the ml output into a peripheral controllable output
7. process_to_ml transforms the user input into an ML input
8. convert_to_bucket converts regular values into bucket data based on interface file settings from the user
9. main : asynchronous driving functio 

### ASYNCHRONICITY

The program is partly asynchronous at the present moment. Notably, async package is used to run some commands in a concurrent fashion, actually passing back and forth function execution when the functions can be idle.

### Debugging
async_trial.py is a debugging unit to make siure that asynchronous execution works as intended

## Log (log.py)
Log contains all the logging utilities and functions to help log data in json files

### Functions
- get_file_size is the size of the file in bytes
- append_dict adds on to the dict keys that are assumed not to be in the dict
- merge_dict is a utility methodn that ios much slower and adds keys uniquely
- log logs the data, either overwriting prior memory location if the file size is to large or appending data if necessary
  
### Debugging
log_test.py tests the functions in log

## Alert (alert.py)
Alert contains all the alert utilities to monitor, raise and log alerts for the user

### Functions
- alert is the collection of alerts raised, which also logs the alert, cretes the message and sends the email as necessary with the correct settings for the email. If configuration.py not included, causes error to halt eecution, if password/username not correct, catches error and does not send email.
- alert_message_generator creates alerts as needed
- log_alert logs an alert
- low_detail_generator generates low detail alerts (only extreme greenhouse conditions)
- high_detail_generator generates high detail alerts (all greenhouse sensor/peripheral output and extremee conditions
- generate_message creatres an email message with subject and body specified by detail waned by user
- send_email sends email to the user at specified email address and password

### CLasses
Also included is a class: AlertStatus
Alert Status is a struct tracking information about alerting and when the previous alert was sent

### Debugging
test_email_alert.py test the functions in alert by sending an email to the intended address

## Pin Constants (pin_constants.py)
Pin constants contains pin information like GPIO pins, register number, channel numbers, light constants, alert constants, other path locations and I2C commands.

### FUnctions
Also included are standard json/pickle utilitie functions used to dump and store data. 

## run_greenhouse.sh
DO NOT USE THIS SCRIPT. THERE IS A MODIFIED SCRIPT TO USE


## Set up to Run
To Run this program, run the command in the directory above
```{bash}
bash start-system.sh
```
The program will start immediately and will not terminate, unless you type in the keyboard ctrl-c, which cause an exception. In addition, this command will also start the UI so that you can manipulate the program. 
