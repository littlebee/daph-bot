#!/usr/bin/env python3
import time
import os
import board
import digitalio
import adafruit_dotstar as dotstar


dataPath = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
ALERT_FILE_PATH = dataPath + "ALERT.txt"

sensor1 = digitalio.DigitalInOut(board.D12)
sensor1.direction = digitalio.Direction.INPUT
sensor1.pull = digitalio.Pull.DOWN

sensor2 = digitalio.DigitalInOut(board.D13)
sensor2.direction = digitalio.Direction.INPUT
sensor2.pull = digitalio.Pull.DOWN

# Braincraft hat has 3 RGB LEDs on it that use the dot star protocol
dots = dotstar.DotStar(board.D6, board.D5, 3, brightness=0.2)

while True:
    if os.path.exists(ALERT_FILE_PATH):
        # I think these are G B R  (why? :/)
        dots[1] = (0, 0, 128)  # center dot red
    else:
        dots[1] = (128, 0, 0)  # center dot green

    if sensor1.value:
        # dim white because these things are blinding me :)
        dots[0] = (64, 64, 64)
    else:
        dots[0] = (0, 0, 0)

    if sensor2.value:
        dots[2] = (64, 64, 64)
    else:
        dots[2] = (0, 0, 0)

    time.sleep(.25)
