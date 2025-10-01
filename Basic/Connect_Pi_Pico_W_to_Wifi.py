# Pi Pico W WiFi Connection Script
# Tested on: October 2, 2025
# Description: Basic WiFi connection for Raspberry Pi Pico W

import network
from time import sleep

ssid = "Capgemini_4G"
password = "MN704116"

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print( 'Connected to ' + ssid + '. ' + 'Device IP: ' + ip )
    return ip

try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
