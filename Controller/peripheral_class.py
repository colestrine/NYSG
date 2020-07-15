"""
peripheral_class copntains classes to manipulate the peripherals in thw greenhouse.
The main package used in this class will be GPIOZero or another package that allows
direct interaction for poins

abstractions for each type of peripheral are presented
in class format

REQUIRES:
- RPi.GPIO in order to use all the GPIO port ufnctionality on the raspberry pi
"""


# -------- DEPENDENT IMPORTS ---------
import gpiozero
import RPi.GPIO as GPIO


# -------- OTHER PACKAGES ----------
import time


# ------- CUSTOM PACKAGES --------
import pin_constants


# ------- CUSTOM CLASSES ------------


class Peripheral:
    """
    Peripheral represents peripheral object

    active is true if the peripheral is on, else false
    """

    def __init__(self, channel, active=False):
        """
        __init__(self, channel, active) constructs a Peripheral in channel channel
        and activity active
        """
        self.channel = channel
        self.active = active

    def set_up(self, resistor_level):
        """
        set_up(self) sets up the pull up or pull down resistor state
        for each Periperhal
        [resistor_level] is whether the resitor is pulled up or down,
        use [GPIO.PUD_UP] to pull up
        """
        GPIO.setup(self.channel, GPIO.IN, GPIO.PUD_UP)

    def change_active(self, activity):
        """
        change_active(self, activity) changes the activity of self
        tp activity

        active is a truthy type, or bool, 1 or true to activate, 0 or false
        to deactivate
        """
        self.active = activity

    def set_active(self):
        """
        set_active(self) sets self to be active
        """
        self.change_active(True)

    def set_inactive(self):
        """
        set_inactive(self) sets peripheral to be inactive
        """
        self.change_active(False)

    def respond(self):
        """
        respond(self) sends the activity state to the physical peripheral
        """
        GPIO.output(self.channel, self.active)

    def read(self):
        """
        Returns the activity state of the peripheral (high/low)
        USE: for debugginf
        """
        return GPIO.input(self.channel)

    def deactivate(self):
        """
        deactivate(self) deactivates the peripheral by closing the channel
        sets active to False

        WARNING: After deactivate is claled, peripheral CANNOT be USED!
        """
        GPIO.cleanup(self.channel)
        self.active = False

    # ----- DEBUGGING TOOLS -----

    def __str__(self):
        """
        __str__(self) is the stringified version of self
        and is the active state of self
        """
        return str(self.active)

    def __repr__(self):
        """
        __str__(self) is the printed version of self
        and is the active state of self
        """
        return str(self.active)


class SolenoidValve(Peripheral):
    """
    SolenoidValve(Peripheral) is a SolenoidValve sensor object
    """

    def __init__(self, channel):
        """
        Creates a Solenoid valve  object with channel chnnale
        """
        super().__init__(channel)


class HeatPad(Peripheral):
    """
    HeatPad(Peripheral) is a Heat Pad sensor object
    """

    def __init__(self, channel):
        """
        Creates a HeatPad  object with channel chnnale
        """
        super().__init__(channel)


class PlantLight(Peripheral):
    """
    PlantLight(Peripheral) is a Plant Light sensor object
    """

    def __init__(self, channel):
        """
        Creates a plant light object with channel chnnale
        """
        super().__init__(channel)


class Fan(Peripheral):
    """
    Fan(Peripheral) is a Fan object
    Freq is hte frequency of the fan; it is a integer, in HZ
    PWM is the pwm object to monitor and change frequency
    dc is the duty_cycle of the pwm

    SUPEF CLaSS: PEripheral
    """

    def __init__(self, channel, freq=0, dc=0):
        """
        Createsa Fan peripheral object with frequency freq
        duty cycles dc, and PWM pwm
        """
        super().__init__(channel)
        self.freq = freq
        self.dc = dc
        self.pwm = GPIO.PWM(self.channel, self.freq)
        self.pwm.start(self.dc)
        self.set_active()

    def set_freq(self, freq):
        """
        set_freq(self, hz) sets the freuqnecy of the fan in freq [hz]
        """
        self.freq = freq
        self.pwm = GPIO.PWM(self.channel, self.freq)

    def get_freq(self):
        """
        get_freq(self) gets the frequency of the Fan in HZ
        """
        return self.freq

    def set_duty_cycle(self, dc):
        """
        set_duty_cycle(self, dc) sets the duty cylce of the fan in [dc] amount
        """
        self.dc = dc

    def get_duty_cycle(self):
        """
        get_duty_cycle(self) gets the duty cycles of the Fan
        """
        return self.dc

    def deactivate(self):
        """
        @ Override:
        Clloses channel, sets actiity to false and runs stop on the pWM
        """
        self.pwm.stop()
        super().deactivate()

    # ----- DEBUGGING TOOLS -----

    def __str__(self):
        """
        @ Override
        __str__(self) is the stringified version of self
        and is the active state of self
        """
        return super().__str__() + " duty cycles : " + str(self.dc) + " frequency in HZ: " + str(self.freq)

    def __repr__(self):
        """
        @ Override
        __str__(self) is the printed version of self
        and is the active state of self, and the duty cyucles and frequency
        """
        return super().__str__() + " duty cycles : " + str(self.dc) + " frequency in HZ: " + str(self.freq)


class Heater(Peripheral):
    """
    Heater represents a Heater object
    Could be different from HEatPad
    TODO: Added as a stub incase we nedd to change for extensionality
    """

    def __init__(self, channel):
        """
        __init__(self, channel) creates a new heater object
        on  GPIO pinnchannel [channel]
        """
        super().__init__(channel)

# ---------- SUMMARY FUNCTIONS ------------


def react_all(ml_results, peripheral_dict):
    """
    react_all(peripheral_dict) changes all the peripherals in the
    [peripheral_dict] based on [ml_results]
    Returns: NONE
    """
    for p in peripheral_dict:
        if p == "valve":
            valve = peripheral_dict[p]
            valve_res = ml_results["valve"]
            valve.set_active(valve_res)
        elif p == "heat":
            heat = peripheral_dict[p]
            heat_res = ml_results["heat"]
            heat.set_active(heat_res)
        elif p == "light":
            light = peripheral_dict[p]
            light_res = ml_results["light"]
            light.set_active(light_res)
        elif p == "fan":
            fan = peripheral_dict[p]
            fan_res = ml_results["fan"]
            fan.set_freq(fan_res)


# ----------- DEBUGGING --------------

def debug_peripheral(log_path, pin_addr, n_iter):
    """
    debug_peripheral(log_path, pin_addr) debugs any peripheral at [pin_addr]
    on GPIO pin and stores results in log_path
    Peripheral cannot be a fan
    """
    GPIO.setup(pin_addr, GPIO.IN, GPIO.PUD_UP)

    log_dict = pin_constants.load_data(log_path)

    for _ in range(n_iter):
        GPIO.output(pin_addr, True)
        time.sleep(5)
        GPIO.output(pin_addr, False)
        time.sleep(5)

        curr_time = time.strftime()
        log_dict[str(curr_time)] = 1

    pin_constants.dump_data(log_dict, log_path)

    GPIO.cleanup(pin_addr)


def debug_fan(log_path, pin_addr, n_iter, freq):
    """
    debug_peripheral(log_path, pin_addr) debugs a fan peripheral at [pin_addr]
    on GPIO pin and stores results in log_path
    """
    GPIO.setup(pin_addr, GPIO.IN, GPIO.PUD_UP)

    log_dict = pin_constants.load_data(log_path)

    pwm = GPIO.PWM(pin_addr, freq)
    for _ in range(n_iter):
        for dc in range(100):
            pwm.start(dc)
            GPIO.output(pin_addr, True)
            time.sleep(5)

        curr_time = time.strftime()
        log_dict[str(curr_time)] = 1

    pin_constants.dump_data(log_dict, log_path)

    GPIO.cleanup(pin_addr)


def read_debug_data(log_path, first_few=None):
    """
    read_debug_data(log_path, first_few) reads in debugged daga at the log_path
    for the first_few characgers, 
    if first_few is None, greads all and prints all to terminal
    """
    data_dict = pin_constants.load_data(log_path)
    dict_list = [(key, data_dict[key]) for key in data_dict]
    if first_few == None:
        first_few = len(dict_list)
    for i in range(min(len(dict_list), first_few)):
        print(dict_list[i][1])
