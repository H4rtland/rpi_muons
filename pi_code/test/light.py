import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(22, 1)


try:
    while True:
        pin_read = GPIO.input(12)
        print("Currently {}".format("light" if pin_read else "dark"))
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting cleanly")
finally:
    GPIO.cleanup()
