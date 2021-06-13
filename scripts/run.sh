#!/usr/bin/env bash

lib/motorControl.py &

cd rpi-vision && . .venv/bin/activate
python3 tests/pitft_labeled_output.py --tflite 2>&1 | ../lib/uniqueThings.py | ../lib/watcher.py

kill $(ps -ef | grep motorControl | awk '{print $2}')