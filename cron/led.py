import RPi.GPIO as GPIO
import time

RED_PIN = 27
BLUE_PIN = 25
GREEN_PIN = 24

def setup_pins():
    """Set up the GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)

def turn_on(PIN):
    GPIO.output(PIN, GPIO.HIGH)

def turn_off(PIN):
    GPIO.output(PIN, GPIO.LOW) 

def cleanup():
    """Clean up the GPIO settings."""
    turn_off(RED_PIN)
    turn_off(GREEN_PIN)
    turn_off(BLUE_PIN)
    GPIO.cleanup()

def flash_twice(PIN):
    try:
        setup_pins()

        turn_on(PIN)
        time.sleep(1)
        turn_off(PIN)
        time.sleep(0.5)
        turn_on(PIN)
        time.sleep(1)
        turn_off(PIN)
    finally:
        cleanup()


def flash_heartbeat(PIN):
    try:
        setup_pins()

        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
        time.sleep(0.25)
        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
        time.sleep(0.25)
        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
        time.sleep(1)

        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
        time.sleep(0.25)
        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
        time.sleep(0.25)
        turn_on(PIN)
        time.sleep(0.25)
        turn_off(PIN)
    finally:
        cleanup()

