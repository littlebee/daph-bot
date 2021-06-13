#!/usr/bin/env python3
import datetime
import os
import sys
import time

dataPath = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
# watcher reads the list of things matched to daphne in this file
DAPHNE_THINGS_FILE_PATH = dataPath + "daphneThings.txt"
# ...and writes out these two files
ALERT_FILE_PATH = dataPath + "ALERT.txt"
SIGHTINGS_FILE_PATH = dataPath + "daphneSightings.txt"


daphneThings = {}
lastDump = time.time()  # seconds

if os.path.exists(ALERT_FILE_PATH):
    os.remove(ALERT_FILE_PATH)

onAlert = False
lastAlert = datetime.datetime.now()


def loadDaphneThings():
    daphneThingsFile = open(DAPHNE_THINGS_FILE_PATH)
    while True:
        line = daphneThingsFile.readline()
        if not line:
            break
        # also can handle the csv output directly from uniqueThings output file
        thing = line.split(',')[0].strip()
        daphneThings[thing] = True
    daphneThingsFile.close()


def logDaphneSighting(thing):
    sightingsFile = open(SIGHTINGS_FILE_PATH, "a")
    sightingsFile.write(
        "Daphne sighting at {}\n".format(lastAlert))
    sightingsFile.close()

    print('got Daphne thing ' + testThing)
    sys.stdout.flush()


def handleAlert():
    print('Daphne alert!')
    f = open(ALERT_FILE_PATH, 'w')
    f.write('I spy, with my one cold electronic eye... Daphne!!')
    f.close()


# Note that when testing, unless the test has 10 seconds worth
# of data (like a lot) this will not get checked unless we
# receive something on stdin
def clearStaleAlert():
    global onAlert
    timeSinceLastAlert = datetime.datetime.now() - lastAlert
    if onAlert and timeSinceLastAlert.total_seconds() > 5:
        onAlert = False
        print('watching...')
        sys.stdout.flush()
        os.remove(ALERT_FILE_PATH)


loadDaphneThings()
print('watching...')

try:
    for thing in iter(sys.stdin.readline, b''):
        clearStaleAlert()
        testThing = thing.rstrip()
        # print('got thing ' + thing + '--')
        if testThing in daphneThings:
            lastAlert = datetime.datetime.now()
            if not onAlert:
                onAlert = True
                logDaphneSighting(thing)
                handleAlert()


except KeyboardInterrupt:
    pass
