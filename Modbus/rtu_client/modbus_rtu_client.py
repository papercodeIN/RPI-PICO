import json
import time
from machine import Pin
from umodbus.serial import Serial as ModbusRTUMaster
from secrets import UART_ID, BAUDRATE, TX_PIN, RX_PIN, CTRL_PIN

# Initialize Modbus RTU master on the specified UART pins
client = ModbusRTUMaster(
    uart_id=UART_ID,
    baudrate=BAUDRATE,
    data_bits=8,
    stop_bits=1,
    parity=None,
    pins=(Pin(TX_PIN), Pin(RX_PIN)),
    ctrl_pin=CTRL_PIN
)

# Load register configuration from JSON file
with open('register.json', 'r') as f:
    registers = json.load(f)

while True:
    try:
        # FC01: Read coils (boolean outputs) from each configured slave
        if 'read_coils' in registers:
            for cfg in registers['read_coils']:
                result = client.read_coils(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], coil_qty=cfg['quantity'])
                print(f'Slave {cfg["slave_addr"]} Read Coils [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result[::-1]}')

        # FC02: Read discrete inputs (boolean inputs) from each configured slave
        if 'read_discrete_inputs' in registers:
            for cfg in registers['read_discrete_inputs']:
                result = client.read_discrete_inputs(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], input_qty=cfg['quantity'])
                print(f'Slave {cfg["slave_addr"]} Read Discrete Inputs [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC03: Read holding registers (read/write 16-bit registers) from each configured slave
        if 'read_holding_registers' in registers:
            for cfg in registers['read_holding_registers']:
                result = client.read_holding_registers(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], register_qty=cfg['quantity'], signed=False)
                print(f'Slave {cfg["slave_addr"]} Read Holding Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC04: Read input registers (read-only 16-bit registers) from each configured slave
        if 'read_input_registers' in registers:
            for cfg in registers['read_input_registers']:
                result = client.read_input_registers(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], register_qty=cfg['quantity'], signed=False)
                print(f'Slave {cfg["slave_addr"]} Read Input Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        # FC05: Write single coil (set one boolean output) on each configured slave
        if 'write_coil' in registers:
            for w in registers['write_coil']:
                result = client.write_single_coil(slave_addr=w['slave_addr'], output_address=w['address'], output_value=w['value'])
                print(f'Slave {w["slave_addr"]} Write Coil [{w["address"]}] = {w["value"]}: {result}')

        # FC15: Write multiple coils (set several boolean outputs at once) on each configured slave
        if 'write_coils' in registers:
            for w in registers['write_coils']:
                result = client.write_multiple_coils(slave_addr=w['slave_addr'], starting_address=w['address'], output_values=w['values'])
                print(f'Slave {w["slave_addr"]} Write Coils [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

        # FC06: Write single holding register (set one 16-bit register) on each configured slave
        if 'write_register' in registers:
            for w in registers['write_register']:
                result = client.write_single_register(slave_addr=w['slave_addr'], register_address=w['address'], register_value=w['value'])
                print(f'Slave {w["slave_addr"]} Write Register [{w["address"]}] = {w["value"]}: {result}')

        # FC16: Write multiple holding registers (set several 16-bit registers at once) on each configured slave
        if 'write_registers' in registers:
            for w in registers['write_registers']:
                result = client.write_multiple_registers(slave_addr=w['slave_addr'], starting_address=w['address'], register_values=w['values'])
                print(f'Slave {w["slave_addr"]} Write Registers [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

    except Exception as e:
        print(f'Error: {e}')

    # Wait before next polling cycle
    time.sleep(5)
