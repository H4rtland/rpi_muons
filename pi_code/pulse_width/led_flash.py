import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)

# GPIO.output(32, 1)

led_on = False
sleep_time = 0.1
on_time = 0.0000005
time_period = 0.08
# print("Frequency: {0:.03f}".format(1/time_period))
# frequency = 20
# time_period = 1/frequency
# on_time = time_period/2
max_total_flashes = total_flashes = 60

st = time.perf_counter()
try:
    """while total_flashes > 0:
        total_flashes -= 1
        GPIO.output(32, 1)
        time.sleep(on_time)
        GPIO.output(32, 0)
        time.sleep(time_period-on_time)
    """
    while True:
        total_flashes -= 1
        led_on = not led_on
        GPIO.output(32, led_on)
        time.sleep(sleep_time)
except KeyboardInterrupt:
    pass
finally:
    t = time.perf_counter()-st
    print("Expected time: {}".format(time_period*max_total_flashes))
    print("Actual time: {}".format(t))
    GPIO.cleanup()
