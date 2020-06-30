"""
Fake class to allow things to work
TODO: get raspberry pi and replace with actual package RPi.GPIO
"""


PUD_UP = True
PUD_DOWN = False

IN = True
OUT = False

BOARD = "board"
BCM = "bcm"


class GPIO:
    def __init__(self):
        pass


class PWM:
    def __init__(self, channel, freq):
        pass

    def start(self, dc):
        pass

    def ChangeFrequency(self, freq):
        pass

    def ChangeDutyCycle(self, dc):
        pass

    def stop(self):
        pass


def setmode(board):
    pass


def input(channel):
    pass


def output(channel, active):
    pass


def cleanup(channel):
    pass


def setup(channel, gpio_in, pull_up_or_down):
    pass
