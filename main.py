import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

# Turn pump on for 1 second
GPIO.output(7, GPIO.HIGH)
time.sleep(1)
GPIO.output(7, GPIO.LOW)
