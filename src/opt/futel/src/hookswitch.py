#!/usr/bin/env python2

import RPi.GPIO as GPIO
import time
import subprocess

PIN=21

GPIO.setmode(GPIO.BCM)          # pin numbering?
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

PLAY_INTRO_CMD = [
    'aplay', '--device=plughw:1,0', '/usr/share/sounds/alsa/Front_Center.wav']

def play_intro():
    subprocess.call(PLAY_INTRO_CMD)

def record():
    pass

def signal_record():
    pass

def hookswitch_up():
    play_intro()
    record()

def hookswitch_down():
    signal_record()

def button_callback(channel):
    if GPIO.input(PIN):
        print("rising")         # release
        hookswitch_up()
    else:
        print("falling")        # push
        hookswitch_down()

GPIO.add_event_detect(PIN,GPIO.BOTH,callback=button_callback)

while True:
    print("cycle")
    time.sleep(60)
