#!/usr/bin/env python3
import datetime
import os
import sys
import time

thisFilePath = os.path.dirname(os.path.abspath(__file__))
dataPath = thisFilePath + '/../data/'
mediaPath = thisFilePath + '/../media/'
logPath = thisFilePath + '/../logs/'

# watcher reads the list of things matched to daphne in this file
daphneThingsFilePath = dataPath + 'daphneThings.txt'
# ...and writes out these two files
alertFilePath = dataPath + 'ALERT.txt'
# ...sound file paths
offFilePath = mediaPath + 'off.mp3'
goodGirlFilePath = mediaPath + 'goodgirl.mp3'
# ...we log sightings to this file
sightingsFilePath = logPath + "daphneSightings.txt"

if os.path.exists(alertFilePath):
    os.remove(alertFilePath)


daphneThings = {}
lastDump = time.time()  # seconds
onAlert = False
lastAlert = datetime.datetime.now()


def loadDaphneThings():
    daphneThingsFile = open(daphneThingsFilePath)
    while True:
        line = daphneThingsFile.readline()
        if not line:
            break
        # also can handle the csv output directly from uniqueThings output file
        thing = line.split(',')[0].strip()
        daphneThings[thing] = True
    daphneThingsFile.close()


def logDaphneSighting(thing):
    sightingsFile = open(sightingsFilePath, "a")
    sightingsFile.write(
        "Daphne sighting at {}\n".format(lastAlert))
    sightingsFile.close()

    print('got Daphne thing ' + testThing)
    sys.stdout.flush()


def handleAlert():
    global onAlert
    onAlert = True

    print('Daphne alert!')
    logDaphneSighting(thing)

    os.system('mpg123 ' + offFilePath)

    f = open(alertFilePath, 'w')
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
        os.system('mpg123 ' + goodGirlFilePath)

        print('watching...')
        sys.stdout.flush()
        os.remove(alertFilePath)


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
                handleAlert()


except KeyboardInterrupt:
    pass
