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
