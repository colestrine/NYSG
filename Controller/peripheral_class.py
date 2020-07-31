"""
peripheral_class copntains classes to manipulate the peripherals in thw greenhouse.
The main package used in this class will be GPIOZero or another package that allows
direct interaction for poins

abstractions for each type of peripheral are presented
in class format
- Peripheral (abstract super class)
- BurstPeripheral (abstract sub class of Peripheral)
- PWMPeripheral (abstract sub class of Burst Peripheral)
- Fan, Light, Heater (concrete subclass of Peripheral)
- SolenoidValve (subclass of burstPeripheral)
- HeatPad (subclass of burst peripheral)

REQUIRES:
- RPi.GPIO in order to use all the GPIO port ufnctionality on the raspberry pi
"""


# -------- DEPENDENT IMPORTS ---------
import RPi.GPIO as GPIO

# -------- OTHER PACKAGES ----------
import datetime

# -------- ASYNC IMPORTS ---------
import asyncio


# ------- CUSTOM PACKAGES --------
from Controller import log
from Controller import pin_constants


# -------- TEST IMPORTS ----------
import sys
import time  # used for callback monitoring
import random


# ------- TEST CONSTANTS ----------
N_PERIPHERALS = 4
N_ITER = 100
PERIPHERAL_LOG_TEST = "PERIPHERAL_LOG_TEST.json"

num_cli_args = len(sys.argv)
if num_cli_args <= 1:
    RUN_TEST = False
else:
    try:
        run_test = True if sys.argv[1].strip().lower() == "true" else False
        RUN_TEST = run_test
    except:
        RUN_TEST = False


# ------- CUSTOM CLASSES ------------


class Peripheral:
    """
    Peripheral represents abstract peripheral object

    ATTRIBUTES:
    active [bool] is true if the peripheral is on, else false
    channel [int] is the GPIO pin channel number the peripheral is hooked up to, e.g. Vent: 40

    INVARIANT: active is true iff voltage is GPIO.HIGH, otherwise active is False iff voltage is GPIO.LOW

    CLASS ATTRIBUTE;
    num_peripherals is number of peripherals created, starts at 0
    When the first peripheral is created, GPIO.BOARD is set, otherwise
    it does not occur for any other peripheral objects
    """

    # number of peripherals
    num_peripherals = 0

    def __init__(self, channel, active=False):  # , burst=pin_constants.BURST):
        """
        __init__(self, channel, active) constructs a Peripheral on channel number channel
        and activity active

        sets up the channel abstraction
        """
        self.channel = channel
        self.set_up()
        self.active = active
        Peripheral.num_peripherals += 1

    def set_up(self, initial_state=GPIO.LOW):
        """
        set_up(self, initial_state) sets up a GPIO channel on channel number self.channel
        with initial_state voltage on the peripheral on GPIO channel number self.channel
        also sets mode to GPIO.BOARD

        RETURNS: NONE
        """
        if Peripheral.num_peripherals == 0:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)  # , initial=initial_state)

    def change_active(self, activity):
        """
        change_active(self, activity) changes the activity of self
        to activity

        activity is a [bool], true if active peripheral, false if inactive

        RETURNS: NONE
        """
        self.active = activity

    async def set_active(self):
        """
        set_active(self) sets self to be active, thus turning on the peripheral at High Voltage
        e.g. Activates peripeheral by outputing GPIO.HIGH, or 3.3 Volts voltage drop
        WARNING: NO BURST: 3.3. Voltes contnuously outpout intil set inactive
        WARNING: DOES NOT SET INACTIVE
        MAINTINA INVARIANT: also sets active status self.active as True, to keep activity = True and voltage as GPIO.HIGH
        RETURNS: NONE
        """
        # change activity to match invariant
        self.change_active(True)
        # change voltage to match invariant
        self.respond(GPIO.HIGH)

    def set_inactive(self):
        """
        set_inactive(self) sets peripheral to be inactive, thus turning off the periperjal to be Low Voltage
        e.g. Deactivates peripeheral by outputing GPIO.LOW or 0 Volts voltage drop
        WARNING: NO BURST: 0 Volts contunously output until periperhal set active again
        WARNING: DOES NOT SET ACTIVE
        MAINTAIN INVARIANT: also sets self.activr as False to keep activity as False and voltage as GPIO.LOW
        RETURNS: NONE
        """
        # change activity to match invariant
        self.change_active(False)
        # change voltage to match invariant
        self.respond(GPIO.LOW)

    def respond(self, voltage_level):
        """
        respond(self) sends the activity state to the physical peripheral
        based on the voltage_level, which is GPIO.HIGH or GPIO.LOW
        on the channel the peripheral is located on

        RAiSES: ASSERTIOMN ERROR Raised if voltage_level is not GPIO>HIGH or GPIO.LOW
        RAISES: ASWERTION ERROR if voltage_level is GPIO.HIGH but self.active is not True
        or voltage_level is GPIO.LOw but self.active is not False
        RETURNS: NONE
        """
        assert voltage_level in [GPIO.HIGH, GPIO.LOW]
        assert (voltage_level, self.active) == (GPIO.HIGH, True) or (
            voltage_level, self.active) == (GPIO.LOW, False)
        GPIO.output(self.channel, voltage_level)

    def read(self):
        """
        Returns the activity state of the peripheral (high/low)
        USE: for debugging
        RETURNS: [bool] activity level: True is active/high voltage, False is inactive/low voltage
        """
        return self.active

    def deactivate(self):
        """
        deactivate(self) deactivates the peripheral by closing the channel and
        sets active to False. voltage set to 0 Volts as well

        WARNING: After deactivate is claled, peripheral CANNOT be USED!
        RETURNS: NONE
        """
        self.set_inactive()
        GPIO.cleanup(self.channel)

    # ----- DEBUGGING TOOLS -----

    def __str__(self):
        """
        __str__(self) is the stringified version of self
        and is the active state of self
        """
        return "Peripheral is : " + str(self.active) + ".\n"

    def __repr__(self):
        """
        __str__(self) is the printed version of self
        and is the active state of self
        """
        return "Peripheral is : " + str(self.active) + ".\n"


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


class BurstPeripheral(Peripheral):
    """
    BurstPeripheral(Peripheral) is a burst peripheral, or a peripheral that activates
    only for a certain amount of time, the burst time

    ATTRIBUTEs;
    burst_time [float]/[None] is the burst time in seconds, floats can include parts of a second
    if burst_time is [NONE], continues forever, never ends the burst until you manually trigger an end
    """

    def __init__(self, channel, burst_time):
        """
        Creates a BurstPeripheral on channel number channel
        with burst_time time for the burst in seconds
        """
        super().__init__(channel)
        self.burst_time = burst_time

    async def set_active(self):
        """
        set_active(self) sets self to be active, thus turning on the peripheral at High Voltage, until burst time ends
        e.g. Activates peripeheral by outputing GPIO.HIGH, or 3.3 Volts voltage drop

        WARNING: if self.burst_time is NONE, continues burst and never sets inactive
        WARNING: HAS BURST: 3.3. Voltes for burst_time, until shut doiwn
        WARNING: SETS BURST
        MAINTINA INVARIANT: also sets active status self.active as True, to keep activity = True and voltage as GPIO.HIGH
        RETURNS: NONE
        """
        # if burst_time is 0, set inactive right away and return
        if self.burst_time == 0:
            self.set_inactive()
            return
        # change activity to match invariant
        self.change_active(True)
        # change voltage to match invariant
        self.respond(GPIO.HIGH)
        # check burst type
        if self.burst_time == None:
            # do not reset if burst_time is NONE
            return
        # wait burst time
        await asyncio.sleep(self.burst_time)
        # time.sleep(self.burst_time)
        # change activity and voltage to match invariant
        self.set_inactive()

    def set_inactive(self):
        """
        set_inactive(self) sets peripheral to be inactive, thus turning off the periperjal to be Low Voltage
        e.g. Deactivates peripeheral by outputing GPIO.LOW or 0 Volts voltage drop
        WARNING: NO BURST: 0 Volts contunously output until periperhal set active again
        WARNING: DOES NOT SET ACTIVE
        MAINTAIN INVARIANT: also sets self.activr as False to keep activity as False and voltage as GPIO.LOW
        RETURNS: NONE
        """
        # change activity to match invariant
        self.change_active(False)
        # change voltage to match invariant
        self.respond(GPIO.LOW)

    def get_burst_time(self):
        """
        get_burst_time(self) hets the burst time in seconds
        RETURNS: [float] burst time in seconds
        """
        return self.burst_time

    def set_burst_time(self, burst_time):
        """
        set_burst_time(self, burst_time) sets the burst time [burst_time] in seconds
        RETURNS: None
        """
        self.burst_time = burst_time

    # ----- DEBUGGING TOOLS -----

    def __str__(self):
        """
        __str__(self) is a string form of the Burst Peripjheral
        """
        return super().__str__() + " Burst Time : " + str(self.burst_time) + " seconds.\n"

    def __repr__(self):
        """
        __repr__(self) is a string form of the Burst Peripjheral
        """
        return super().__str__() + " Burst Time : " + str(self.burst_time) + " seconds.\n"


class SolenoidValve(BurstPeripheral):
    """
    SolenoidValve(Peripheral) is a SolenoidValve sensor object

    IS A BURSTPERIPHERAL
    """

    def __init__(self, channel, burst_time=pin_constants.BURST):
        """
        Creates a Solenoid valve  object with channel chnnale
        """
        super().__init__(channel, burst_time)


class HeatPad(BurstPeripheral):
    """
    HeatPad(Pwm_Peripheral) is a Heat Pad sensor object
    SUbclass of PWM_PERIPHERAL
    """

    def __init__(self, channel, burst_time=pin_constants.BURST):
        """
        Creates a HeatPad  object with channel chnnale
        """
        super().__init__(channel, burst_time)


class Fan(BurstPeripheral):
    """
    Fan(BurstPeripheral) is a Fan object

    SUPERCLASS: BurstPeripheral
    """

    def __init__(self, channel, burst_time=pin_constants.BURST):
        """
        Createsa Fan peripheral object
        """
        super().__init__(channel, burst_time)


class Pwm_Peripheral(BurstPeripheral):
    """
    Pwm_Peripheral(Peripheral) is a peripheral with a pwm controller
    and burst_time burst_time
    """

    def __init__(self, channel, burst_time, freq=0, dc=0):
        """
        Createsa PWM peripheral object with frequency freq
        duty cycles dc, and PWM pwm and burst_time burst_time
        """
        super().__init__(channel, burst_time)
        self.freq = freq
        self.dc = dc
        self.pwm = GPIO.PWM(self.channel, freq)
        self.pwm.start(self.dc)

    def set_freq(self, freq):
        """
        set_freq(self, hz) sets the freuqnecy of the pwm peripheral in freq [hz]
        """
        self.freq = freq
        self.pwm = self.pwm.ChangeFrequency(freq)

    def get_freq(self):
        """
        get_freq(self) gets the frequency of the pwm peripheral in HZ
        """
        return self.freq

    def set_duty_cycle(self, dc):
        """
        set_duty_cycle(self, dc) sets the duty cylce of the pwm peripheral in [dc] amount
        """
        self.dc = dc
        self.pwm = self.pwm.ChangeDutyCycle(dc)

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
        return super().__str__() + " duty cycles : " + str(self.dc) + " frequency in HZ: " + str(self.freq) + ".\n"

    def __repr__(self):
        """
        @ Override
        __str__(self) is the printed version of self
        and is the active state of self, and the duty cyucles and frequency
        """
        return super().__str__() + " duty cycles : " + str(self.dc) + " frequency in HZ: " + str(self.freq) + ".\n"


class PlantLight(Pwm_Peripheral):
    """
    PlantLight(Peripheral) is a Plant Light sensor object

    A PWM BURST Peripheral
    """

    def __init__(self, channel, burst_time=None, freq=pin_constants.FREQ, dc=pin_constants.DC):
        """
        Creates a plant light object with channel chnnale
        """
        super().__init__(channel, burst_time, freq, dc)


# ---------- SUMMARY FUNCTIONS ------------


def translate_action_to_burst_time(action):
    """
    translate_action_to_burst_time() translates a 0 to 4 action to a burstime
    """
    if action == 0:
        return pin_constants.NO_ACTION
    elif action == 1:
        return pin_constants.BIG_DECREASE
    elif action == 2:
        return pin_constants.SMALL_DECREASE
    elif action == 3:
        return pin_constants.SMALL_INCREASE
    elif action == 4:
        return pin_constants.BIG_INCREASE


async def change_peripheral(peripheral, action):
    """
    change_peripheral(peripheral, burst_time) changes peripheral to burst time
    and activates and deactivates as necessary
    """
    burst_time = translate_action_to_burst_time(action)

    if isinstance(peripheral, BurstPeripheral):
        peripheral.set_burst_time(burst_time)
        await peripheral.set_active()
    else:
        # not a burst peripheral
        if burst_time != 0:
            await peripheral.set_active()
        else:
            peripheral.set_inactive()


async def react_all(ml_results, peripheral_dict):
    """
    react_all(peripheral_dict) changes all the peripherals in the
    [peripheral_dict] based on [ml_results]
    Returns: NONE
    """
    valve = None
    heat = None
    light = None
    fan = None
    valve_res = None
    heat_res = None
    light_res = None
    fan_res = None
    for p in peripheral_dict:
        if p == "water":
            valve = peripheral_dict[p]
            valve_res = ml_results["water"]
        elif p == "heat":
            heat = peripheral_dict[p]
            heat_res = ml_results["heat"]
        elif p == "light":
            light = peripheral_dict[p]
            light_res = ml_results["light"]
        elif p == "fan":
            fan = peripheral_dict[p]
            fan_res = ml_results["fan"]

    await asyncio.gather(change_peripheral(valve, valve_res), change_peripheral(heat, heat_res), change_peripheral(light, light_res), change_peripheral(fan, fan_res))

    # for p in peripheral_dict:
    #     if p == "water":
    #         valve = peripheral_dict[p]
    #         valve_res = ml_results["water"]
    #         if valve_res:
    #             valve.set_active()
    #         else:
    #             valve.set_inactive()
    #     elif p == "heat":
    #         heat = peripheral_dict[p]
    #         heat_res = ml_results["heat"]
    #         if heat_res:
    #             heat.set_active()
    #         else:
    #             heat.set_inactive()
    #     elif p == "light":
    #         light = peripheral_dict[p]
    #         light_res = ml_results["light"]
    #         if light_res:
    #             light.set_active()
    #         else:
    #             light.set_inactive()
    #     elif p == "fan":
    #         fan = peripheral_dict[p]
    #         fan_res = ml_results["fan"]
    #         if fan_res:
    #             fan.set_active()
    #         else:
    #             fan.set_inactive()


# ------------ MANUAL CONTROL -------------------------

def manual(peripheral_dict, action_list):
    """
    manual(peripheral_dict, cction_dict) allows for mannual control of peripherals
    peripheral_dict is a dictionary of peripherals, with keys "water", :heat", light"
    and "fan

    action_list is a list of pairs where the first element is the name of the action and
    the second is the action itself

    Intended to be used by the User interface as manualk control

    Returns None
    """
    def bistate_set(obj, action):
        if action == "activate":
            obj.set_active()
        elif action == "inactive":
            obj.set_inactive()

    valve = peripheral_dict["water"]
    heater = peripheral_dict["heat"]
    light = peripheral_dict["light"]
    fan = peripheral_dict["fan"]

    for action_name, action in action_list:
        if action_name == "water":
            bistate_set(valve, action)
        elif action_name == "heater":
            bistate_set(heater, action)
        elif action_name == "light":
            bistate_set(light, action)
        elif action_name == "fan":
            bistate_set(fan, action)


# ----------- DEBUGGING --------------


def debug_peripheral(log_path, peripheral_type, n_iter):
    """
    debug_peripheral(log_path, peripheral_type, n_iter) debugs any peripheral peripheral_type
    on GPIO pin and stores results in log_path for n_iters of data
    """

    if peripheral_type == "heat":
        peripheral = HeatPad(pin_constants.HEAT)
    elif peripheral_type == "light":
        peripheral = PlantLight(pin_constants.LED)
    elif peripheral_type == "water":
        peripheral = SolenoidValve(pin_constants.VALVE)
    elif peripheral_type == "fan":
        peripheral = Fan(pin_constants.VENT)
    else:
        raise RuntimeError(
            "Not a recognized peripheral : " + str(peripheral_type))

    log_dict = {}

    for _ in range(n_iter):
        peripheral.set_active()
        time.sleep(5)
        peripheral.set_inactive()
        time.sleep(5)

        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")

        log_dict[current_time] = peripheral.read()

    peripheral.deactivate()
    pin_constants.dump_data(log_dict, log_path)


def fan_turn_on_test():
    """
    fan_turn_on_test() tests turning ona  fan for 20 second sthan off
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_constants.VENT, GPIO.OUT, initial=GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin_constants.VENT, GPIO.LOW)
    GPIO.cleanup(pin_constants.VENT)


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


# ---------- WEEK 1 DEMO TEST PERIPHERAL LOGGING -------------
def test_peripheral_logging(n_iter, log_path):
    """
    test_peripheral_logging(n_iter) logs peripheral actions for n_iter
    at log_path in JSON form

    WARNING: THIS DEMO ONLY CHECKS LOGGING CAPABILITIES
    """
    time_dict = {}

    for _iter in range(n_iter):
        # get time
        now = datetime.datetime.now()
        # add second and microsecond
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")

        actions = []
        for _ in range(N_PERIPHERALS):
            peripheral_action = random.randint(0, 1)
            actions.append(peripheral_action)

        peripherals = ["heat", "light", "fan", "water"]
        combined_list = list(zip(peripherals, actions))
        combined_dict = {key[0]: key[1] for key in combined_list}

        time_dict[current_time] = combined_dict

    log.log(log_path, time_dict, log.MAX_SIZE)


# ---------- MAIN TESTING --------------------
if __name__ == "__main__":
    if RUN_TEST:
        fan_turn_on_test()
        debug_peripheral('Debug_peripheral_path.json', "fan", 100)
        debug_peripheral('Debug_peripheral_path.json', "heat", 100)
        debug_peripheral('Debug_peripheral_path.json', "light", 100)
        debug_peripheral('Debug_peripheral_path.json', "water", 100)
        read_debug_data('Debug_peripheral_path.json')
