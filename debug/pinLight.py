#!/usr/bin/env python3

#
# This is a simple utility to monitor pins 12 & 13 (digital) and light
# the first and last led on the braincraft hat when the corresponding
# pin is high (12 - left; 13 right)
#
# usage:
#   pinLight.py


import time
import board
import digitalio
import adafruit_dotstar as dotstar


sensor1 = digitalio.DigitalInOut(board.D12)
sensor1.direction = digitalio.Direction.INPUT
sensor1.pull = digitalio.Pull.DOWN


sensor2 = digitalio.DigitalInOut(board.D13)
sensor2.direction = digitalio.Direction.INPUT
sensor2.pull = digitalio.Pull.DOWN

# Braincraft hat has 3 RGB LEDs on it that use the dot star protocol
dots = dotstar.DotStar(board.D6, board.D5, 3, brightness=0.2)

lastLow1 = lastLow2 = lastHigh1 = lastHigh2 = time.time()
lastSensor1Value = lastSensor2Value = False

while True:
    if sensor1.value:
        dots[0] = (128, 128, 128)
        if not lastSensor1Value:
            lastSensor1Value = True
            lastHigh1 = time.time()
            print('D12 high; ' + str(lastHigh1 - lastLow1))
    else:
        dots[0] = (0, 0, 0)
        if lastSensor1Value:
            lastSensor1Value = False
            lastLow1 = time.time()
            print('D12 low; ' + str(lastLow1 - lastHigh1))

    if sensor2.value:
        dots[2] = (128, 128, 128)
        if not lastSensor2Value:
            lastSensor2Value = True
            lastHigh2 = time.time()
            print('D13 high; ' + str(lastHigh2 - lastLow2))
    else:
        dots[2] = (0, 0, 0)
        if lastSensor2Value:
            lastSensor2Value = False
            lastLow2 = time.time()
            print('D13 low; ' + str(lastLow2 - lastHigh2))

    time.sleep(.1)
