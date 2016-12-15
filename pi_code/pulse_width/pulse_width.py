import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(22, 1)

on_time = 0
currently_on = False

def event_pulse(pin):
    global on_time, currently_on
    on = GPIO.input(pin)
    if on and not currently_on:
        on_time = time.perf_counter()
        currently_on = True
    elif currently_on:
        currently_on = False
        print("Pulse duration: {}".format(time.perf_counter()-on_time))
        


GPIO.add_event_detect(12, GPIO.RISING, bouncetime=10)
GPIO.add_event_callback(12, event_pulse)

try:
    time.sleep(300)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
