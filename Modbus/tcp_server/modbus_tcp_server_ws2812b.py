from umodbus.tcp import ModbusTCP
import time
from machine import Pin
import network
from neopixel import NeoPixel
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SERVER_PORT

# Connect to WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')

# Use port from secrets configuration
tcp_port = MODBUS_SERVER_PORT
local_ip = station.ifconfig()[0]

# Configure WS2812B LED strip on GPIO 16 with 10 LEDs
NUM_LEDS = 10
PIN_LED = 16
led = NeoPixel(Pin(PIN_LED), NUM_LEDS)

# Initialize Modbus TCP server instance
server = ModbusTCP()
is_bound = False

# Bind server to local IP and port if not already bound
is_bound = server.get_bound_status()

if not is_bound:
    server.bind(local_ip=local_ip, local_port=tcp_port)

# Callback to control individual WS2812B LEDs based on holding register writes
# Value 1 = green, value 2 = red, any other value = off
def LED_cb(reg_type, address, val):
    led_index = address
    if val[0] == 1:
        led[led_index] = (0, 255, 0)
    elif val[0] == 2:
        led[led_index] = (255, 0, 0)
    else:
        led[led_index] = (0, 0, 0)
    led.write()

# Create one holding register per LED (addresses 0 through NUM_LEDS-1)
register_definitions = {
    "HREGS": {
        f"LED_{i}": {"register": i, "len": 1, "val": 0, "on_set_cb": LED_cb, "on_get_cb": LED_cb}
        for i in range(NUM_LEDS)
    }
}

# Setup registers and start serving
print('Setting up registers ...')
server.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as Modbus TCP server on {}:{}'.format(local_ip, tcp_port))

# Main loop: process incoming Modbus TCP requests
while True:
    try:
        result = server.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP server...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as server")
