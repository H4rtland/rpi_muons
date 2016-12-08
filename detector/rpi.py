# run rpi detection code here
# preferably running interrupts
# need some way to preserve state
# maybe a class would be nice

import RPi.GPIO as GPIO
import time
import tempfile

print("Setting up RPi code")

GPIO.setmode(GPIO.BOARD)

# potential divider
GPIO.setup(22, GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# status LED
GPIO.setup(32, GPIO.OUT)

GPIO.output(22, 1)

class LPD:
    running = False
    start_time = 0
    stop_time = 0
    pulses = 0
    pulse_times = []

    @staticmethod
    def start():
        LPD.running = True
        LPD.start_time = time.perf_counter()
        LPD.pulses = 0
        LPD.pulse_times = []
        GPIO.output(32, 1)

    @staticmethod
    def stop():
        GPIO.output(32, 0)
        LPD.running = False
        LPD.stop_time = time.perf_counter()
        file = tempfile.NamedTemporaryFile(delete=False)
        filename = file.name
        file.close()
        with open(filename, "w") as file:
            for t in LPD.pulse_times:
                file.write("{}\r\n".format(t))

        return filename
            
    @staticmethod
    def running_for():
        return time.perf_counter() - LPD.start_time

    @staticmethod
    def running_for_hms():
        t = LPD.running_for()
        h, m = divmod(t, 3600)
        m, s = divmod(m, 60)
        return int(h), int(m), s
    
    @staticmethod
    def light_pulse_callback(call):
        if LPD.running and GPIO.input(12):
            dt = time.perf_counter() - LPD.start_time
            LPD.pulse_times.append(dt)
            LPD.pulses += 1
            # print("Pulsing")
            

GPIO.add_event_detect(12, GPIO.RISING, bouncetime=10)
GPIO.add_event_callback(12, LPD.light_pulse_callback)
