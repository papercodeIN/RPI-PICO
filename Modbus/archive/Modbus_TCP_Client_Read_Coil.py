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

coil_address = 0
coil_qty = 5
coil_status = modbus_client.read_coils(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=coil_address, coil_qty=coil_qty)
print('Status of COIL from {} to {} : {}'.format(coil_address, coil_address + coil_qty, coil_status[::-1]))
