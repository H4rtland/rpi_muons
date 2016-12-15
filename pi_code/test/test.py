import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

print("Ready")

GPIO.setup(22, GPIO.OUT)

on_state = False

try:
    while True:
        on_state = not on_state
        GPIO.output(22, 1)
        print("On" if on_state else "Off")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting cleanly")
finally:
    GPIO.cleanup()
