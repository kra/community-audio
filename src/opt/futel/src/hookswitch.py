#!/usr/bin/env python2

import RPi.GPIO as GPIO
import datetime
import subprocess
import sys
import time

PIN=21

GPIO.setmode(GPIO.BCM)          # pin numbering?
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

record_child = None

# XXX should die on device busy?
PLAY_INTRO_CMD = [
    'aplay',
    '--device=plughw:1,0',
    '/usr/share/sounds/alsa/Front_Center.wav']

# XXX should die on device busy?
RUN_RECORD_CMD = [
    'arecord',
    '--device=plughw:1,0',
    '--format',
    'S16_LE',
    '--rate',
    '44100',
    '-c1',
    '--duration',
    '600']

def log(line):
    print(line)
    sys.stdout.flush()

def record_file_path():
    return '/'.join(['/mnt/futel',
                     datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S%f')])

def play_intro():
    subprocess.call(PLAY_INTRO_CMD)

def record():
    global record_child
    if record_child is not None:
        log("recording child exists, not recording")
    else:
        #terminate_record()
        run_record_cmd = RUN_RECORD_CMD + [record_file_path()]
        record_child = subprocess.Popen(run_record_cmd)

def terminate_record():
    global record_child
    if record_child is None:
        log("no recording child to terminate")
    else:
        record_child.terminate()
    record_child = None

def hookswitch_up():
    log("hookswitch_up")
    if record_child is None:
        play_intro()
    else:
        log("recording child detected during hookswitch_up")
    record()

def hookswitch_down():
    log("hookswitch_down")
    terminate_record()

def button_callback(channel):
    if GPIO.input(PIN):
        log("rising")         # release switch
        hookswitch_down()
    else:
        log("falling")        # contact switch
        hookswitch_up()

GPIO.add_event_detect(PIN, GPIO.BOTH, callback=button_callback)

while True:
    log("cycle")
    # could check and stop recording if hookswitch released, but the time limit
    # makes this less important
    time.sleep(5)
