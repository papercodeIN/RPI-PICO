import json
import time
import network
from umodbus.tcp import TCP as ModbusTCPMaster
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SLAVE_IP, MODBUS_SLAVE_PORT, MODBUS_SLAVE_ADDR

# Connect to WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')

# Load register configuration from JSON file
with open('register.json', 'r') as f:
    registers = json.load(f)

# Initialize Modbus TCP client connection to the slave device
client = ModbusTCPMaster(slave_ip=MODBUS_SLAVE_IP, slave_port=MODBUS_SLAVE_PORT, timeout=5)

while True:
    try:
        # FC01: Read coils (boolean outputs)
        if 'read_coils' in registers:
            cfg = registers['read_coils']
            result = client.read_coils(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], coil_qty=cfg['quantity'])
            print(f'Read Coils [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result[::-1]}')

        # FC02: Read discrete inputs (boolean inputs)
        if 'read_discrete_inputs' in registers:
            cfg = registers['read_discrete_inputs']
            result = client.read_discrete_inputs(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], input_qty=cfg['quantity'])
            print(f'Read Discrete Inputs [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC03: Read holding registers (read/write 16-bit registers)
        if 'read_holding_registers' in registers:
            cfg = registers['read_holding_registers']
            result = client.read_holding_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], register_qty=cfg['quantity'])
            print(f'Read Holding Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC04: Read input registers (read-only 16-bit registers)
        if 'read_input_registers' in registers:
            cfg = registers['read_input_registers']
            result = client.read_input_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_addr=cfg['address'], register_qty=cfg['quantity'])
            print(f'Read Input Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC05: Write single coil (set one boolean output)
        if 'write_coil' in registers:
            for w in registers['write_coil']:
                result = client.write_single_coil(slave_addr=MODBUS_SLAVE_ADDR, output_address=w['address'], output_value=w['value'])
                print(f'Write Coil [{w["address"]}] = {w["value"]}: {result}')

        # FC15: Write multiple coils (set several boolean outputs at once)
        if 'write_coils' in registers:
            for w in registers['write_coils']:
                result = client.write_multiple_coils(slave_addr=MODBUS_SLAVE_ADDR, starting_address=w['address'], output_values=w['values'])
                print(f'Write Coils [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

        # FC06: Write single holding register (set one 16-bit register)
        if 'write_register' in registers:
            for w in registers['write_register']:
                result = client.write_single_register(slave_addr=MODBUS_SLAVE_ADDR, register_address=w['address'], register_value=w['value'])
                print(f'Write Register [{w["address"]}] = {w["value"]}: {result}')

        # FC16: Write multiple holding registers (set several 16-bit registers at once)
        if 'write_registers' in registers:
            for w in registers['write_registers']:
                result = client.write_multiple_registers(slave_addr=MODBUS_SLAVE_ADDR, starting_address=w['address'], register_values=w['values'])
                print(f'Write Registers [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

    except Exception as e:
        print(f'Error: {e}')

    # Wait before next polling cycle
    time.sleep(5)
