<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [daph-bot](#daph-bot)
  - [Things you'll need to buy or find](#things-youll-need-to-buy-or-find)
  - [Things you'll need to do](#things-youll-need-to-do)
  - [But how does it work??](#but-how-does-it-work)
    - [rpi-vision/tests/pitft_labeled_output.py --tflite](#rpi-visiontestspitft_labeled_outputpy---tflite)
    - [lib/uniqueThings.py](#libuniquethingspy)
    - [lib/watcher.ph](#libwatcherph)
    - [lib/motorControl.py](#libmotorcontrolpy)
  - [More things to do](#more-things-to-do)
    - [Start daph-bot when the PI reboots](#start-daph-bot-when-the-pi-reboots)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# daph-bot

A robot to detect when Daphne (my year old husky mix) is on the counter that uses image recognition via Tensor Flow Lite.

## Things you'll need to buy or find

1. [Raspberry PI 4](https://www.adafruit.com/product/4564). Tensor Flow will fully tap one of the 4 cpu cores of the arm 71 on the PI 4

2. [Raspberry PI 4 camera](https://www.adafruit.com/product/3099)

3. [Adafruit Braincraft Hat](https://www.adafruit.com/product/4374). This little hat is packed with features we will make use.

4. [Adafruit DC & Stepper Motor Hat](https://www.adafruit.com/product/2348). Any I2C DC motor driver will work.

5. [A little speaker](https://www.adafruit.com/product/3351). <- this one comes with a JST connector that will plug right into the Braincraft hat

6. [2 x Basic PIR sensor](https://www.adafruit.com/product/4667). We'll use these to tell when there is motion in the periphery of view and rotate daph-bot toward the action.

7. [2 x UBEC DC to DC stepdown](https://www.adafruit.com/product/1385). We'll use separate stepdowns for the PI and the motors

8. [A robot frame with 2 DC motors](https://www.adafruit.com/product/2939). I used one like this that I got from IDK where, but the base was bigger than I wanted so I 3D printed my own.

9. [Stemma QT 4 pin plug](https://www.adafruit.com/product/4209). We'll use this to get I2C, 3.3V and Gnd to the motor controller hat.

10. [Some Risers](https://www.adafruit.com/product/3299) to stack things up

11. Some spare wires in different colors

## Things you'll need to do

1. [Setup the PI for headless use and install things](https://learn.adafruit.com/adafruit-braincraft-hat-easy-machine-learning-for-raspberry-pi/raspberry-pi-setup). Continue to the next page from there to setup Blinka, Audio, Fan, Display Module, Camera,

2. [Setup Tensorflow Lite on the PI](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4) Follow on with the next pages from there to setup Tensor flow. When finished you should be able to run the following commands from the pi home directory

```
sudo bash
cd rpi-vision && . .venv/bin/activate
python3 tests/pitft_labeled_output.py --tflite
```

And see the data (guesses) tensor flow is seeing. The code for daph-bot will use the output of the command above to detect when Daphne is present.

3. Install some more software

On the raspberry PI:

```
sudo pip3 install adafruit-circuitpython-motorkit adafruit-circuitpython-dotstar
```

To get sound working and .mp3 files to play, I needed to install some additional debian packages:

```
sudo apt-get install libasound2-plugins
sudo apt-get install mpg123
```

4. Init ssh key and create data and logs directories

Copying your SSH public key to the PI user's authorized_keys files.

See scripts/init.sh for example meant to be run from Mac terminal. If you edit `HOSTNAME` to match your `user@raspberry.local`, you should be able to use the script.

If you didn't use the script above, don't forget to create the data directory. For example, on the PI in the pi user home directory,

```
mkdir -p data
mkdir -p logs
```

5. Copy directories from this repository

From your computer, copy the following directories with files to the PI user's home directory. See, for example, `scripts/upload.sh`

Be sure to copy the following directories:

- data/
- lib/
- media/
- scripts/

When you log into your PI as pi@yourraspberry.local you should see these directories using the ls command

```
ls
```

## But how does it work??

There are 4 semi independent python programs running that make daph-bot work. (The paths are from the /home/pi directory on the raspberry)

### rpi-vision/tests/pitft_labeled_output.py --tflite

This was installed as part of setting up Tensor Flow Lite. See, Things You'll Need To Do, above.

It's output looks like,

```
INFO:root:TFLite inference took 100 ms, 9.9 FPS
INFO:root:[('n03207941', 'dishwasher', 0.17871304), ('n03761084', 'microwave', 0.16713606), ('n04590129', 'window_shade', 0.10856207), ('n04404412', 'television', 0.03231336), ('n03201208', 'dining_table', 0.024060488)]
```

It is controlling the camera and the LCD display, passing about 10fps of image to Tensor Flow and writting a stream of log information to `stderr`. Instead of digging into how to create machine learning models or how that program works or is maintained, let's just treat it like a black box and pipe it's output to another program....

### lib/uniqueThings.py

This should probably be called parse things. It parses the output from pitft_labeled_output.py

After a few seconds without any sightings, it removes data/ALERT.txt.

uniqueThings.py also keeps a log of unique things seen and their counts (logs/uniqueThings.txt) so you can generate your own data/daphneThings.txt. You can just point daph-bot's camera at your furry friend and then edit the logs/uniqueThings.txt file to remove any lines that are obviously not.

uniqueThings.py writes each thing it sees, whether it has seen it or not, to it's `stdout`.

### lib/watcher.ph

This python program takes the stream of things from uniqueThings.py one per line looks for any sightings of Daphne things (data/daphneThings.txt) in the stream of image recognition data.

When it gets a match on a Daphne thing, it creates file (data/ALERT.txt) to signal motor control and anyone (you) debugging that it has an sighting and logs the sighting to logs/daphneSightings.txt for debugging.

### lib/motorControl.py

This program interfaces with the Raspberry GPIO to control the motors of daph-bot.

It continuously checks for

- when both PIR sensors on GPIO 12 (left) and GPIO 13 (right) are hot, then stop moving and let the pixie dust settle
- when the left PIR sensor is hot and right is cold, then rotate left to bring the action into view
- when the right PIR sensor is hot and left is cold, then rotate right to bring the action into view
- when the data/ALERT.txt file created by watcher.py exists, then do a little quick forward / backward motion and light the center LED red

## More things to do

### Start daph-bot when the PI reboots

1. SSH to the raspberry PI and edit the /etc/rc.local file

```
sudo nano /etc/rc.local
```

2. Add the following to rc.local. Just before the `exit 0` add

```
# send stdout and stderr from rc.local to a log file
exec 1>/home/pi/data/rc.local.log 2>&1
set -x

cd /home/pi && /home/pi/scripts/run.sh
```

3. Save and close the file. When back at the shell prompt, chg the mode of the /etc/rc.local file to make it executable

```
sudo chmod +x /etc/rc.local
```

That's it! Try it out

```
sudo reboot now
```
