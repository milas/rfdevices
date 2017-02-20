# Introduction
High level RF library for interacting with common devices.

# Requirements
* Python 3
* Native GPIO library (see Installation)

# Installation
Clone this repo locally, then:  
```bash
pip install rfdevices
```

## Native GPIO Library
For GPIO operations, this library uses [adafruit/Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)
for compatibility with multiple SoC boards. As a result, you'll need to ensure you manually install your platform's
GPIO library.

If you have a Raspberry Pi:
```bash
pip install RPi.GPIO
```
See [RPi.GPIO on Sourceforge](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) for more information. 

If you have a Beaglebone Black:
```bash
pip install Adafruit_BBIO
```
See [adafruit/adafruit-beaglebone-io-python](https://github.com/adafruit/adafruit-beaglebone-io-python) for more information.

If you have an Intel (e.g. Galileo, Edison) board, follow the instructions at
[intel-iot-devkit/mraa](https://github.com/intel-iot-devkit/mraa).


# Usage
After installing, the `rfsend` tool will be available in your `PATH`.

Here's an example of sending a command to a UC7070T (Harbor Breeze) fan to toggle the light on/off:
```bash
# GPIO pin 23 / fan dipswitch set to 1101
rpi-rftx -g 23 -t uc7070t -b 111010000001
```

# Credits
This was originally forked from [`milaq/rpi-rf`](https://github.com/milaq/rpi-rf).

Portions of the code are:  
Copyright (c) 2016 Suat Özgür, Micha LaQua  
Copyright (c) 2017 Milas Bowman
