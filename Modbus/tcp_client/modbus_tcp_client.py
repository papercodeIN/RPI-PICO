import json
import time
import network
from umodbus.tcp import TCP as ModbusTCPMaster
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SLAVE_IP, MODBUS_SLAVE_PORT, MODBUS_SLAVE_ADDR

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')

with open('register.json', 'r') as f:
    registers = json.load(f)

client = ModbusTCPMaster(slave_ip=MODBUS_SLAVE_IP, slave_port=MODBUS_SLAVE_PORT, timeout=5)

while True:
    try:
        if 'read_coils' in registers:
            cfg = registers['read_coils']
            result = client.read_coils(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], coil_qty=cfg['quantity'])
            print(f'Read Coils [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result[::-1]}')

        if 'read_discrete_inputs' in registers:
            cfg = registers['read_discrete_inputs']
            result = client.read_discrete_inputs(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], input_qty=cfg['quantity'])
            print(f'Read Discrete Inputs [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'read_holding_registers' in registers:
            cfg = registers['read_holding_registers']
            result = client.read_holding_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], register_qty=cfg['quantity'])
            print(f'Read Holding Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'read_input_registers' in registers:
            cfg = registers['read_input_registers']
            result = client.read_input_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], register_qty=cfg['quantity'])
            print(f'Read Input Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'write_coil' in registers:
            for w in registers['write_coil']:
                result = client.write_single_coil(slave_addr=MODBUS_SLAVE_ADDR, output_address=w['address'], output_value=w['value'])
                print(f'Write Coil [{w["address"]}] = {w["value"]}: {result}')

        if 'write_coils' in registers:
            for w in registers['write_coils']:
                result = client.write_multiple_coils(slave_addr=MODBUS_SLAVE_ADDR, starting_address=w['address'], output_values=w['values'])
                print(f'Write Coils [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

        if 'write_register' in registers:
            for w in registers['write_register']:
                result = client.write_single_register(slave_addr=MODBUS_SLAVE_ADDR, register_address=w['address'], register_value=w['value'])
                print(f'Write Register [{w["address"]}] = {w["value"]}: {result}')

        if 'write_registers' in registers:
            for w in registers['write_registers']:
                result = client.write_multiple_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_address=w['address'], register_values=w['values'])
                print(f'Write Registers [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

    except Exception as e:
        print(f'Error: {e}')

    time.sleep(5)
