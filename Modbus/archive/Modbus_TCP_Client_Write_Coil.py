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
print(f'Updating data to Modbus TCP Server at {MODBUS_SLAVE_IP}:{MODBUS_SLAVE_PORT}')

coil_address = 0
new_coil_val = 0
operation_status = modbus_client.write_single_coil(slave_addr=MODBUS_SLAVE_ADDR, output_address=coil_address, output_value=new_coil_val)
print('Result of setting COIL {}: {}'.format(coil_address, operation_status))
