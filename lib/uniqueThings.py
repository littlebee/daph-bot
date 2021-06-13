#!/usr/bin/env python3
import os
import re
import sys
import time

#
# This script takes the output from tensorflow test progam and
# parses out the thing names in the data to stdout.  T
#
# It also creates ../data/uniqueThings.txt which is a CSV file
# of unique things seen and the number of times seen.   You
# can use the uniqueThings.txt output to build a new data/daphneThings.txt
# used by watcher.py

uniqueThings = {}

# e.g.  INFO:root:[('n03207941', 'dishwasher', 0.18921205), ('n03761084', 'microwave', 0.14883143), ('n04590129', 'window_shade', 0.12404499), ('n04404412', 'television', 0.026665367), ('n03201208', 'dining_table', 0.025589854)]
regex = re.compile("\('[^']*', '([^']*)'")
lastDump = time.time()  # seconds

dataPath = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
outFilePath = dataPath + 'uniqueThings.txt'

# clear the output file
f = open(outFilePath, "w")
f.write("")
f.close()

try:
    for line in iter(sys.stdin.readline, b''):
        currentTime = time.time()
        # every 5 seconds or so, dump the unique counts
        if currentTime - lastDump > 5:
            f = open(outFilePath, "w")
            for k, v in uniqueThings.items():
                f.write("" + k + "," + str(v) + "\n")
            f.flush()
            f.close()
            lastDump = currentTime

        if line != "":
            matches = re.findall(regex, line)
            for thing in matches:
                # the downstream pipe, watcher.py, is expecting a
                # constant stream of things, not just unique
                print(thing)
                sys.stdout.flush()

                if thing in uniqueThings:
                    matchedThingCount = uniqueThings[thing]
                    uniqueThings[thing] = matchedThingCount + 1
                else:
                    uniqueThings[thing] = 1


except KeyboardInterrupt:
    if not f.closed:
        f.flush()
        f.close()
