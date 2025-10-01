# Pi Pico W Simple LED Blinking Script
# Tested on: October 2, 2025
# Description: Simple LED blinking program for Raspberry Pi Pico W onboard LED

#Simple LED Blinking Program

from machine import Pin
from time import sleep
myLED = Pin('LED',Pin.OUT)
while 1:
    myLED.on()
    sleep(1)
    myLED.off()
    sleep(1)
