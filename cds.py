import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin = 18

def discharge():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)


def charge_time():
    t1 - time.time()
    GPIO.setup(pin, GPIO.IN)
    while not GPIO.input(pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        time.sleep(0.001)
        GPIO.setup(pin, GPIO.IN)
        time.sleep(0.001)
    t2 = time.time()
    return (t2 - t1)*1000000


def analog_read():
    discharge()
    return charge_time()

while True:
    print(analog_read())
    time.sleep(0.5)
