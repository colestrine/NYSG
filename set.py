import RPi.GPIO as GPIO
from Controller.pin_constants import VENT,LED,VALVE,HEAT

GPIO.setmode(GPIO.BCM)

GPIO.setup(VENT, GPIO.OUT, 0)
GPIO.setup(HEAT, GPIO.OUT, 0)
GPIO.setup(VALVE, GPIO.OUT, 0)
GPIO.setup(LED, GPIO.OUT, 0)

input("Hit any key to end set.py")

GPIO.cleanup()