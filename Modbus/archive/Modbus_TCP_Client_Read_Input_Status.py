import time
from umodbus.tcp import TCP as ModbusTCPMaster
import network
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SLAVE_IP, MODBUS_SLAVE_PORT, MODBUS_SLAVE_ADDR

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')

modbus_client = ModbusTCPMaster(slave_ip=MODBUS_SLAVE_IP, slave_port=MODBUS_SLAVE_PORT, timeout=5)
print(f'Requesting data from Modbus TCP Server at {MODBUS_SLAVE_IP}:{MODBUS_SLAVE_PORT}')

ist_address = 0
input_qty = 1
input_status = modbus_client.read_discrete_inputs(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=ist_address, input_qty=input_qty)
print('Status of IST from {} to {} : {}'.format(ist_address, ist_address + input_qty, input_status))
