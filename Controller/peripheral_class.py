import gpiozero

"""
peripheral_class copntains classes to manipulate the peripherals in thw greenhouse.
The main package used in this class will be GPIOZero or another package that allows
direct interaction for poins

abstractions for each type of peripheral are presented
in class format 
"""


class Peripheral:
    """
    Peripheral represents peripheral object

    active is true if the peripheral is on, else false
    """

    def __init__(self, active=False):
        """
        __init__(self, active=False) constructs a Peripheral with active = active
        """
        self.active = active

    def change_active(self, activity):
        """
        change_active(self, activity) changes the activity of self
        tp activity
        """
        self.active = activity

    def set_active(self):
        """
        set_active(self) sets self to be active
        """
        self.change_active(True)

    def set_inactive(self):
        """
        set_inactive(self) sets self to be inactive
        """
        self.change_active(False)

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

    def __init__(self):
        super().__init__()


class HeatPad(Peripheral):
    """
    HeatPad(Peripheral) is a Heat Pad sensor object
    """

    def __init__(self):
        super().__init__()


class PlantLight(Peripheral):
    """
    PlantLight(Peripheral) is a Plant Light sensor object
    """

    def __init__(self):
        super().__init__()


class Fan(Peripheral):
    """
    Fan(Peripheral) is a Fan object 
    Freq is hte frequency of the fan; it is a integer
    """

    def __init__(self, freq=0):
        super().__init__()
        self.freq = freq
