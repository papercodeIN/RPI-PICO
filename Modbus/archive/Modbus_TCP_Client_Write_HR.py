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

hreg_address = 5
new_hreg_val = 44
operation_status = modbus_client.write_single_register(slave_addr=MODBUS_SLAVE_ADDR, register_address=hreg_address, register_value=new_hreg_val)
print('Result of setting HREG {}: {}'.format(hreg_address, operation_status))
