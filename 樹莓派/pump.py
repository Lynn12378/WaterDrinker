import RPi.GPIO as GPIO
import time

def outflow(sec):
    Relay_Ch3 = 17
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Relay_Ch3,GPIO.OUT)

    try:
        #Control the Channel 3
        GPIO.output(Relay_Ch3,GPIO.LOW)
        time.sleep(sec)
        GPIO.output(Relay_Ch3,GPIO.HIGH)
    except KeyboardInterrupt:
        print("stop")
    finally:
        GPIO.cleanup()

