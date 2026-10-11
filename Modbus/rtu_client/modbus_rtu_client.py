import json
import time
from machine import Pin
from umodbus.serial import Serial as ModbusRTUMaster
from secrets import UART_ID, BAUDRATE, TX_PIN, RX_PIN, CTRL_PIN

client = ModbusRTUMaster(
    uart_id=UART_ID,
    baudrate=BAUDRATE,
    data_bits=8,
    stop_bits=1,
    parity=None,
    pins=(Pin(TX_PIN), Pin(RX_PIN)),
    ctrl_pin=CTRL_PIN
)

with open('register.json', 'r') as f:
    registers = json.load(f)

while True:
    try:
        if 'read_coils' in registers:
            for cfg in registers['read_coils']:
                result = client.read_coils(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], coil_qty=cfg['quantity'])
                print(f'Slave {cfg["slave_addr"]} Read Coils [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result[::-1]}')

        if 'read_discrete_inputs' in registers:
            for cfg in registers['read_discrete_inputs']:
                result = client.read_discrete_inputs(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], input_qty=cfg['quantity'])
                print(f'Slave {cfg["slave_addr"]} Read Discrete Inputs [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'read_holding_registers' in registers:
            for cfg in registers['read_holding_registers']:
                result = client.read_holding_registers(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], register_qty=cfg['quantity'], signed=False)
                print(f'Slave {cfg["slave_addr"]} Read Holding Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'read_input_registers' in registers:
            for cfg in registers['read_input_registers']:
                result = client.read_input_registers(slave_addr=cfg['slave_addr'], starting_addr=cfg['address'], register_qty=cfg['quantity'], signed=False)
                print(f'Slave {cfg["slave_addr"]} Read Input Registers [{cfg["address"]}:{cfg["address"] + cfg["quantity"]}]: {result}')

        if 'write_coil' in registers:
            for w in registers['write_coil']:
                result = client.write_single_coil(slave_addr=w['slave_addr'], output_address=w['address'], output_value=w['value'])
                print(f'Slave {w["slave_addr"]} Write Coil [{w["address"]}] = {w["value"]}: {result}')

        if 'write_coils' in registers:
            for w in registers['write_coils']:
                result = client.write_multiple_coils(slave_addr=w['slave_addr'], starting_address=w['address'], output_values=w['values'])
                print(f'Slave {w["slave_addr"]} Write Coils [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

        if 'write_register' in registers:
            for w in registers['write_register']:
                result = client.write_single_register(slave_addr=w['slave_addr'], register_address=w['address'], register_value=w['value'])
                print(f'Slave {w["slave_addr"]} Write Register [{w["address"]}] = {w["value"]}: {result}')

        if 'write_registers' in registers:
            for w in registers['write_registers']:
                result = client.write_multiple_registers(slave_addr=w['slave_addr'], starting_address=w['address'], register_values=w['values'])
                print(f'Slave {w["slave_addr"]} Write Registers [{w["address"]}:{w["address"] + len(w["values"])}] = {w["values"]}: {result}')

    except Exception as e:
        print(f'Error: {e}')

    time.sleep(5)
