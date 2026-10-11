# Modbus TCP Client

Reads and writes coils, discrete inputs, holding registers, and input registers on a single Modbus TCP slave device. All operations are configured via `register.json`.

## Files

| File | Purpose |
|------|---------|
| `modbus_tcp_client.py` | Main script |
| `register.json` | Full read + write configuration (active) |
| `register_read_only.json` | Sample: read operations only |
| `register_write_only.json` | Sample: write operations only |
| `secrets.example.py` | Credentials template |

## Setup

1. Install the Modbus library on your Pico W (via Thonny Shell):
```python
import mip
mip.install("github:brainelectronics/micropython-modbus")
```

2. Copy `secrets.example.py` to `secrets.py` and fill in your values:
```python
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"
MODBUS_SLAVE_IP = "192.168.1.50"
MODBUS_SLAVE_PORT = 502
MODBUS_SLAVE_ADDR = 1
```

3. Edit `register.json` to configure operations. Remove any key to skip that operation. Sample configs are provided:
- `register_read_only.json` — read-only example (copy to `register.json` to use)
- `register_write_only.json` — write-only example (copy to `register.json` to use)

### Read Configuration

```json
{
    "read_coils": {"address": 0, "quantity": 5},
    "read_discrete_inputs": {"address": 0, "quantity": 1},
    "read_holding_registers": {"address": 0, "quantity": 5},
    "read_input_registers": {"address": 0, "quantity": 10}
}
```

| Key | Function Code | Description |
|-----|--------------|-------------|
| `read_coils` | FC01 | Read coil status |
| `read_discrete_inputs` | FC02 | Read discrete input status |
| `read_holding_registers` | FC03 | Read holding registers |
| `read_input_registers` | FC04 | Read input registers |

### Write Configuration

```json
{
    "write_coil": [{"address": 0, "value": true}],
    "write_coils": [{"address": 0, "values": [true, false, true]}],
    "write_register": [{"address": 0, "value": 100}],
    "write_registers": [{"address": 0, "values": [100, 200, 300]}]
}
```

| Key | Function Code | Description |
|-----|--------------|-------------|
| `write_coil` | FC05 | Write single coil (`value`: `true`/`false`) |
| `write_coils` | FC15 | Write multiple coils (`values`: array of `true`/`false`) |
| `write_register` | FC06 | Write single holding register (`value`: integer) |
| `write_registers` | FC16 | Write multiple holding registers (`values`: array of integers) |

Each write key accepts an array, so you can write to multiple addresses per cycle.

4. Upload `modbus_tcp_client.py`, `register.json`, and `secrets.py` to the Pico W.

5. Run `modbus_tcp_client.py` from Thonny. The script executes all configured operations every 5 seconds.
