#!/usr/bin/env python3
import time
import os
import board
import digitalio
import adafruit_dotstar as dotstar
from adafruit_motorkit import MotorKit

dataPath = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
ALERT_FILE_PATH = dataPath + "ALERT.txt"

MAX_THROTTLE = 1
MIN_THROTTLE = 0.6  # This is the minimum for my rig before the motors fail to move it

# these values are dtermined by the speed of the motors and the sensor trigger time
ROTATION_SEC = 0.25
ROTATION_PAUSE = 1.5

motors = MotorKit(i2c=board.I2C())
leftMotor = motors.motor1
rightMotor = motors.motor2

leftMotor.throttle = 0
rightMotor.throttle = 0

sensor1 = digitalio.DigitalInOut(board.D12)
sensor1.direction = digitalio.Direction.INPUT
sensor1.pull = digitalio.Pull.DOWN

sensor2 = digitalio.DigitalInOut(board.D13)
sensor2.direction = digitalio.Direction.INPUT
sensor2.pull = digitalio.Pull.DOWN
# Braincraft hat has 3 RGB LEDs on it that use the dot star protocol
dots = dotstar.DotStar(board.D6, board.D5, 3, brightness=0.2)


def stopMoving():
    leftMotor.throttle = 0
    rightMotor.throttle = 0


def rotateLeft():
    leftMotor.throttle = -1 * MIN_THROTTLE
    rightMotor.throttle = MIN_THROTTLE
    time.sleep(ROTATION_SEC)
    stopMoving()
    time.sleep(ROTATION_PAUSE)


def rotateRight():
    leftMotor.throttle = MIN_THROTTLE
    rightMotor.throttle = -1 * MIN_THROTTLE
    time.sleep(ROTATION_SEC)
    stopMoving()
    time.sleep(ROTATION_PAUSE)


def updateLEDs():
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


while True:
    updateLEDs()

    if sensor1.value == sensor2.value:
        stopMoving()

        if sensor1.value:
            # give IR sensors time to reset
            time.sleep(4)
    else:
        if sensor1.value:
            rotateLeft()
        elif sensor2.value:
            rotateRight()

    time.sleep(.25)
