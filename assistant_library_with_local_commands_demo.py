#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_FORWARD_LEFT_PIN = 13	# IN1 - Forward Drive
PWM_REVERSE_LEFT_PIN = 5	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_FORWARD_RIGHT_PIN = 26	# IN1 - Forward Drive
PWM_REVERSE_RIGHT_PIN = 6	# IN2 - Reverse Drive


GPIO.setup(PWM_FORWARD_RIGHT_PIN,GPIO.OUT)
GPIO.setup(PWM_REVERSE_RIGHT_PIN,GPIO.OUT) 
GPIO.setup(PWM_FORWARD_LEFT_PIN,GPIO.OUT)
GPIO.setup(PWM_REVERSE_LEFT_PIN,GPIO.OUT)

my_pwmFL = GPIO.PWM(PWM_FORWARD_RIGHT_PIN,100)
my_pwmRL = GPIO.PWM(PWM_REVERSE_RIGHT_PIN,100)
my_pwmFR = GPIO.PWM(PWM_FORWARD_LEFT_PIN,100)
my_pwmRR = GPIO.PWM(PWM_REVERSE_LEFT_PIN,100)


GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
GPIO.output(PWM_REVERSE_LEFT_PIN, 0)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    my_pwmFL.start(0)
    my_pwmRL.start(0)
    my_pwmFR.start(70)
    my_pwmRR.start(70)
    time.sleep(5)
    my_pwmFL.start(0)
    my_pwmRL.start(0)
    my_pwmFR.start(0)
    my_pwmRR.start(0)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))

def go_forward():
    my_pwmFL.start(40)
    my_pwmRL.start(0)
    my_pwmFR.start(40)
    my_pwmRR.start(0)
    time.sleep(5)
    my_pwmFL.start(0)
    my_pwmRL.start(0)
    my_pwmFR.start(0)
    my_pwmRR.start(0)
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 1)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 1)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 0)
    #time.sleep(2)
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 0)

def go_back():
    my_pwmFL.start(0)
    my_pwmRL.start(40)
    my_pwmFR.start(0)
    my_pwmRR.start(40)
    time.sleep(5)
    my_pwmFL.start(0)
    my_pwmRL.start(0)
    my_pwmFR.start(0)
    my_pwmRR.start(0)
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 1)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 1)
    #time.sleep(2)
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 0)

#def allStop():
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 0)
    #my_pwmFL.start(0)
    #my_pwmRL.start(0)
    #my_pwmFR.start(0)
    #my_pwmRR.start(0)
    
    #forwardLeft.value = 0
    #reverseLeft.value = 0
    #forwardRight.value = 0
    #reverseRight.value = 0
 
#def forwardDrive():
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 1)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 0)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 1)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 0)
    #my_pwmFL.start(50)
    #my_pwmRL.start(0)
    #my_pwmFR.start(50)
    #my_pwmRR.start(0)
    #forwardLeft.value = 1.0
    #reverseLeft.value = 0
    #forwardRight.value = 1.0
    #reverseRight.value = 0
 
#def reverseDrive():
    #GPIO.output(PWM_FORWARD_RIGHT_PIN, 0)
    #GPIO.output(PWM_REVERSE_RIGHT_PIN, 1)
    #GPIO.output(PWM_FORWARD_LEFT_PIN, 0)
    #GPIO.output(PWM_REVERSE_LEFT_PIN, 1)
    #my_pwmFL.start(0)
    #my_pwmRL.start(50)
    #my_pwmFR.start(0)
    #my_pwmRR.start(50)
    #forwardLeft.value = 0
    #reverseLeft.value = 1.0
    #forwardRight.value = 0
    #reverseRight.value = 1.0
 
#def spinLeft():
    #my_pwmFL.start(0)
    #my_pwmRL.start(50)
    #my_pwmFR.start(50)
    #my_pwmRR.start(0)
    #forwardLeft.value = 0
    #reverseLeft.value = 1.0
    #forwardRight.value = 1.0
    #reverseRight.value = 0

#def SpinRight():
    #my_pwmFL.start(50)
    #my_pwmRL.start(0)
    #my_pwmFR.start(0)
    #my_pwmRR.start(50)
    #forwardLeft.value = 1.0
    #reverseLeft.value = 0
    #forwardRight.value = 0
    #reverseRight.value = 1.0
 
#def forwardTurnLeft():
    #my_pwmFL.start(10)
    #my_pwmRL.start(0)
    #my_pwmFR.start(70)
    #my_pwmRR.start(0)
    #forwardLeft.value = 0.2
    #reverseLeft.value = 0
    #forwardRight.value = 0.8
    #reverseRight.value = 0
 
#def forwardTurnRight():
    #my_pwmFL.start(70)
    #my_pwmRL.start(0)
    #my_pwmFR.start(10)
    #my_pwmRR.start(0)
    #forwardLeft.value = 0.8
    #reverseLeft.value = 0
    #forwardRight.value = 0.2
    #reverseRight.value = 0
 
#def reverseTurnLeft():
    #my_pwmFL.start(0)
    #my_pwmRL.start(10)
    #my_pwmFR.start(0)
    #my_pwmRR.start(70)
    #forwardLeft.value = 0
    #reverseLeft.value = 0.2
    #forwardRight.value = 0
    #reverseRight.value = 0.8
 
#def reverseTurnRight():
    #my_pwmFL.start(0)
    #my_pwmRL.start(70)
    #my_pwmFR.start(0)
    #my_pwmRR.start(10)
    #forwardLeft.value = 0
    #reverseLeft.value = 0.8
    #forwardRight.value = 0
    #reverseRight.value = 0.2

def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reset':
            assistant.stop_conversation()
            go_back()
        elif text == 'forward':
            assistant.stop_conversation()
            go_forward()
        elif text == 'back':
            go_back()
            assistant.stop_conversation()
        elif text == 'left':
            go_back()
        elif text == 'right':
            reboot_pi()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
