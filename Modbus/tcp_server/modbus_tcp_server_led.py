from umodbus.tcp import ModbusTCP
import time
from machine import Pin
import network
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SERVER_PORT

myLED = Pin('LED', Pin.OUT)

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')
tcp_port = MODBUS_SERVER_PORT
local_ip = station.ifconfig()[0]

# ModbusTCP can get TCP requests from a host device to provide/set data
client = ModbusTCP()
is_bound = False

# check whether client has been bound to an IP and port
is_bound = client.get_bound_status()

if not is_bound:
    client.bind(local_ip=local_ip, local_port=tcp_port)

def LED_cb(reg_type, address, val):
    if int(val[0]) == 1:myLED.on()
    elif int(val[0]) == 0:myLED.off()

# commond slave register setup, to be used with the Master example above
register_definitions = {"COILS": {"LED": {"register": 0,"len": 1,"val": 0}}}

register_definitions['COILS']['LED']['on_set_cb'] = LED_cb
register_definitions['COILS']['LED']['on_get_cb'] = LED_cb


print('Setting up registers ...')
client.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as Modbus TCP server on {}:{}'.format(local_ip, tcp_port))

while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP server...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as server")
