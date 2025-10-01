# Pi Pico W WiFi Access Point Creation Script
# Tested on: October 2, 2025
# Description: Creates a WiFi Access Point on Raspberry Pi Pico W

import socket
import network

ssid = "Pi Pico W AP"
password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password) 
ap.active(True)

while ap.active == False:
  pass

print("Access point active")
print(ap.ifconfig())
