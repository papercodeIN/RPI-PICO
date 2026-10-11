from umodbus.tcp import ModbusTCP
import time
from machine import Pin
import network
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SERVER_PORT

# Configure onboard LED as output
myLED = Pin('LED', Pin.OUT)

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

# Initialize Modbus TCP server instance
server = ModbusTCP()
is_bound = False

# Bind server to local IP and port if not already bound
is_bound = server.get_bound_status()

if not is_bound:
    server.bind(local_ip=local_ip, local_port=tcp_port)

# Callback to control onboard LED based on coil write value
def LED_cb(reg_type, address, val):
    if int(val[0]) == 1:
        myLED.on()
    elif int(val[0]) == 0:
        myLED.off()

# Define a single coil register at address 0 for LED control
register_definitions = {"COILS": {"LED": {"register": 0, "len": 1, "val": 0}}}

# Attach callbacks so LED state changes on write and can be read back
register_definitions['COILS']['LED']['on_set_cb'] = LED_cb
register_definitions['COILS']['LED']['on_get_cb'] = LED_cb

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
