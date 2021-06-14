#!/usr/bin/env bash
set -x

HOST=pi@trainerbot.local

scp -r ./data/daphneThings.txt $HOST:/home/pi/data
scp -r ./scripts $HOST:/home/pi
scp -r ./media $HOST:/home/pi
scp -r ./lib $HOST:/home/pi