# Introduction
High level RF library for interacting with common devices.

# Requirements
* Python 3
* RPi.GPIO

# Installation
Clone this repo locally, then:  
```bash
pip install rfdevices
```

# Usage
After installing, the `rfsend` tool will be available in your `PATH`.

Here's an example of sending a command to a UC7070T (Harbor Breeze) fan to toggle the light on/off:
```bash
# GPIO pin 23
# Fan dipswitches are 1101
rpi-rftx -g 23 -t uc7070t -b 111010000001
```

# Credits
This was originally forked from [`milaq/rpi-rf`](https://github.com/milaq/rpi-rf).

Portions of the code are:  
Copyright (c) 2016 Suat Özgür, Micha LaQua  
Copyright (c) 2017 Milas Bowman
