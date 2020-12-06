# MicroPython

# Install tools (esptool, adafruit-ampy)

You can use conda or whatever tools you like to work with when preparing your python environment.

As always I use virtualenv to setup a local development environment:

``` bash
$ virtualenv venv
$ . ./venv/bin/activate

$ pip install -r requirements.txt
```


# Upload micropython

I use the esptool.py to upload the micropython firmware to the microcontroller.

To clean all existing stuff from the ESP8266:

``` bash
$ esptool.py --port /dev/ttyUSB0 erase_flash
```

Get the micropython firmware [here](http://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin).

``` bash
$ esptool.py  --port /dev/ttyUSB0 --baud 460800 write_flash -fm dio --flash_size=detect 0 esp8266-20191220-v1.12.bin
```


# Terminal

Normally during development I power my wemos D1 mini boards via a USB mini cable. Conveniently a serial connection is available using the same cable to check what is going on on the board.

I use picocom (because screen gives me some trouble):

$ picocom --baud 115200 /dev/ttyUSB0

exit with CTRL-A-X


# Work with the micropython board

At least two options are available:

* micropython pyboard.py
* adafruit-ampy

I am currently using adafruit-ampy because it has the nicer command line.

To install ampy:

$ pip install adafruit-ampy


# Pinout

Careful the pin numbers used in micropython might differ to what you are used to. Please check in advance:

[pinout](https://micropython-on-wemos-d1-mini.readthedocs.io/en/latest/basics.html)


# Sample "main.py"

``` python
from time import sleep
from machine import Pin

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)
while True: 
    led1.on()
    led2.off()
    sleep(0.5)
    led1.off()
    led2.on()
    sleep(0.5)
```


# Run the sample script

The 'run' command runs the program on the ESP8266 one time only. 

$ ampy --port /dev/ttyUSB0 run main.py


# Install the program on the board

Once you reset or power down the board the previous run ends and your script is gone. 
To make it more permanent (and install the script on the microcontroller) do the following:

$ ampy --port /dev/ttyUSB0 put main_blinker.py main.py

You can use picocom to check what is going on:

$ picocom --baud 115200 /dev/ttyUSB0

exit with CTRL-A-X


If you follow the convention to name the script "main.py" for uploading that is all you have to do. The main.py script is installed on the microcontroller. After a reset it starts running.

Removing the script is simple, too:

$ ampy --port /dev/ttyUSB0 rm main.py


# Production setup

What I have shown to you above is the "development setup". Of cause you would want to have a firmware without python console prohibiting the upload of files etc.

please find more information about a production build [here](
https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/build-firmware#compile-micropython-firmware-2-33).
