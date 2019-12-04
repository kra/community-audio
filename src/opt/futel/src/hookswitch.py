#!/usr/bin/env python2

import RPi.GPIO as GPIO
import time

PIN=21

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_callback(channel):
    if GPIO.input(PIN):
        print("rising")
    else:
        print("falling")
    print("Button was pushed!")

GPIO.add_event_detect(PIN,GPIO.BOTH,callback=button_callback)

while True:
    print("cycle")
    time.sleep(60 * 60)
