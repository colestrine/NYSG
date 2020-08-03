from Controller.peripheral_class import fan_turn_on_test
from Controller.pin_constants import LED
import RPi.GPIO as GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.LOW) # turn off light
    fan_turn_on_test()
