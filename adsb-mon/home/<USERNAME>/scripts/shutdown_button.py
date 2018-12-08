#!/bin/python
# Script for powering an "On" LED for as long as the system is running,
# while waiting for the button press to eventually shutdown the system.

##################################################################
## ADS-B-monitor
## Copyright (C) 2017  Loxia labs
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details:
## <http://www.gnu.org/licenses/>.
###################################################################


import RPi.GPIO as GPIO
import time
import os


# Setup the button pin in reading mode and with pullups enabled. (Broadcom SOC Pin numbers)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# Setup LED pin as output and turn it on
GPIO.setup(31, GPIO.OUT)
GPIO.output(31, True)


def Simmerdown(numTimes=10, speed=0.15):
    for i in range(0, numTimes):
        GPIO.output(31, False)
        time.sleep(speed)
        GPIO.output(31, True)
        time.sleep(speed)
    GPIO.cleanup()	# When blinking ends LED stays lit until system shutdown pulls the plug


def Shutdown(channel):
    Simmerdown()			# First blink alarmingly
    os.system("sudo shutdown -h now")   # Now we can die in peace


# Function to execute when the button pressed event is detected
GPIO.add_event_detect(18, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)


while 1:
    time.sleep(1)
