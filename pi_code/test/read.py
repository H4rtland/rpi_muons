import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(22, 1)

start_time = None
presses = 0

def button_callback(call):
    global start_time, presses
    if start_time is None:
        start_time = time.perf_counter()
    pressed_at_time = time.perf_counter() - start_time
    presses += 1
    print("Button pushed at time t = {0:.02f}, press rate = {1:.02f} presses/sec".format(pressed_at_time, presses/pressed_at_time))

GPIO.add_event_detect(12, GPIO.RISING, bouncetime=100)
GPIO.add_event_callback(12, button_callback)


try:
    while True:
        # pin_read = GPIO.input(12)
        # print("Button {}".format("pressed" if pin_read else "not pressed"))
        time.sleep(0.1)
        if not start_time is None:
            if time.perf_counter()-start_time > 30:
                print("Time up final rate: {0:.02f}".format(presses/30))
                raise KeyboardInterrupt
except KeyboardInterrupt:
    print("Exiting cleanly")
finally:
    GPIO.cleanup()
