import RPi.GPIO as GPIO
from Controller.pin_constants import VENT,LED,VALVE,HEAT

GPIO.setmode(GPIO.BCM)

GPIO.setup(VENT, GPIO.OUT)
GPIO.output(VENT, 0)
GPIO.setup(HEAT, GPIO.OUT)
GPIO.output(HEAT, 0)
GPIO.setup(VALVE, GPIO.OUT)
GPIO.output(VALVE, 0)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED,0)

input("Hit any key to end set.py")

GPIO.cleanup()
