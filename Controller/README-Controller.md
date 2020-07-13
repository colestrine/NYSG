# NYSG 2020

## Controller

- Raspberry Pi 4
- 40 GPIO pins

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

## Sensor Classes

### Description

The sensor class represents a sensor abstraction, that can turn on and off a sensor
and read from the sensor. The Sensor object is meant to be compatiable with I2C

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



