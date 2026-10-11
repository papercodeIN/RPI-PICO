# Modbus RTU Client

Reads and writes coils, discrete inputs, holding registers, and input registers on one or more Modbus RTU slave devices over UART/RS485. All operations are configured via `register.json`. Supports multi-slave setups where each operation targets a specific slave address.

## Files

| File | Purpose |
|------|---------|
| `modbus_rtu_client.py` | Main script |
| `register.json` | Register read/write configuration with per-operation slave addresses |
| `secrets.example.py` | Hardware configuration template |
| `Pi Pico W  Modbus Serial Connection.png` | Wiring diagram |

## Wiring

![Wiring Diagram](Pi%20Pico%20W%20%20Modbus%20Serial%20Connection.png)

```
Pico W GP0 (TX) → RS485 DI
Pico W GP1 (RX) → RS485 RO
Pico W GP2      → RS485 DE/RE (direction control, optional)
GND → GND, 3.3V → VCC
```

## Setup

1. Install the Modbus library on your Pico W (via Thonny Shell):
```python
import mip
mip.install("github:brainelectronics/micropython-modbus")
```

2. Copy `secrets.example.py` to `secrets.py` and fill in your values:
```python
UART_ID = 0
BAUDRATE = 9600
TX_PIN = 0
RX_PIN = 1
CTRL_PIN = None
```

Set `CTRL_PIN` to the GPIO pin number connected to RS485 DE/RE if using a transceiver (e.g. `2`). Set to `None` for direct UART connection.

3. Edit `register.json` to configure operations. Remove any key to skip that operation. Each entry requires a `slave_addr` field to target a specific device on the bus.

### Read Configuration

All read keys accept an array of objects, allowing you to poll multiple slaves or multiple register ranges per cycle.

```json
{
    "read_coils": [
        {"slave_addr": 1, "address": 0, "quantity": 5}
    ],
    "read_discrete_inputs": [
        {"slave_addr": 1, "address": 0, "quantity": 1}
    ],
    "read_holding_registers": [
        {"slave_addr": 1, "address": 0, "quantity": 5},
        {"slave_addr": 2, "address": 0, "quantity": 3}
    ],
    "read_input_registers": [
        {"slave_addr": 1, "address": 0, "quantity": 10}
    ]
}
```

| Key | Function Code | Description |
|-----|--------------|-------------|
| `read_coils` | FC01 | Read coil status |
| `read_discrete_inputs` | FC02 | Read discrete input status |
| `read_holding_registers` | FC03 | Read holding registers |
| `read_input_registers` | FC04 | Read input registers |

### Write Configuration

All write keys accept an array of objects, allowing you to write to multiple slaves per cycle.

```json
{
    "write_coil": [
        {"slave_addr": 1, "address": 0, "value": true}
    ],
    "write_coils": [
        {"slave_addr": 1, "address": 0, "values": [true, false, true]}
    ],
    "write_register": [
        {"slave_addr": 1, "address": 0, "value": 100},
        {"slave_addr": 2, "address": 0, "value": 200}
    ],
    "write_registers": [
        {"slave_addr": 1, "address": 0, "values": [100, 200, 300]}
    ]
}
```

| Key | Function Code | Description |
|-----|--------------|-------------|
| `write_coil` | FC05 | Write single coil (`value`: `true`/`false`) |
| `write_coils` | FC15 | Write multiple coils (`values`: array of `true`/`false`) |
| `write_register` | FC06 | Write single holding register (`value`: integer) |
| `write_registers` | FC16 | Write multiple holding registers (`values`: array of integers) |

### Multi-Slave Example

To poll two different devices on the same RS485 bus, use different `slave_addr` values:

```json
{
    "read_holding_registers": [
        {"slave_addr": 1, "address": 0, "quantity": 3},
        {"slave_addr": 2, "address": 0, "quantity": 3},
        {"slave_addr": 3, "address": 10, "quantity": 1}
    ],
    "write_coil": [
        {"slave_addr": 1, "address": 0, "value": true},
        {"slave_addr": 2, "address": 0, "value": false}
    ]
}
```

Each object in the array is executed sequentially. This allows one Pico W to communicate with any number of slaves sharing the same bus.

4. Upload `modbus_rtu_client.py`, `register.json`, and `secrets.py` to the Pico W.

5. Run `modbus_rtu_client.py` from Thonny. The script executes all configured operations every 5 seconds.

</content>