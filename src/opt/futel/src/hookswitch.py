#!/usr/bin/env python2

import RPi.GPIO as GPIO
import datetime
import subprocess
import time

PIN=21

GPIO.setmode(GPIO.BCM)          # pin numbering?
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

record_child = None

PLAY_INTRO_CMD = [
    'aplay',
    '--device=plughw:1,0',
    '/usr/share/sounds/alsa/Front_Center.wav']

# XXX time limit
RUN_RECORD_CMD = [
    'arecord',
    '--device=plughw:1,0',
    '--format',
    'S16_LE',
    '--rate',
    '44100',
    '-c1',
    '/opt/futel/var/test.wav']

def filename():
    return datetime.datetime.now().isoformat()

def play_intro():
    subprocess.call(PLAY_INTRO_CMD)

def record():
    global record_child
    record_child = subprocess.Popen(RUN_RECORD_CMD)

def terminate_record():
    global record_child
    if record_child is None:
        print("no recording child")
    else:
        record_child.terminate()
    record_child = None

def hookswitch_up():
    play_intro()
    record()

def hookswitch_down():
    terminate_record()

def button_callback(channel):
    if GPIO.input(PIN):
        print("rising")         # release
        hookswitch_up()
    else:
        print("falling")        # push
        hookswitch_down()

GPIO.add_event_detect(PIN, GPIO.BOTH, callback=button_callback)

while True:
    print("cycle")
    # XXX should check and stop recording if hookswitch released
    time.sleep(1)
