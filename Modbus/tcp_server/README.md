# Modbus TCP Server

Exposes coils, discrete inputs, holding registers, and input registers for Modbus TCP clients to read/write. Includes examples with callbacks, onboard LED control, and WS2812B LED control.

## Files

| File | Purpose |
|------|---------|
| `modbus_tcp_server_callbacks.py` | Full server example with register callbacks |
| `modbus_tcp_server_led.py` | Control onboard LED via coil writes |
| `modbus_tcp_server_ws2812b.py` | Control WS2812B LEDs via holding register writes |
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
MODBUS_SERVER_PORT = 502
```

3. Upload the desired server script and `secrets.py` to the Pico W.

4. Run the script from Thonny. The Pico W will connect to WiFi and start listening for Modbus TCP requests.

## Examples

### Callbacks (`modbus_tcp_server_callbacks.py`)

Demonstrates `on_set_cb` and `on_get_cb` callbacks for all register types. Modify `register_definitions` dict in the script to change exposed registers. Test with any Modbus TCP client (QModMaster, ModbusPoll, or `tcp_client/` from this repo) connecting to `<pico_ip>:<port>`.

### Onboard LED (`modbus_tcp_server_led.py`)

Write coil at address 0 to control the Pico W onboard LED:
- Value `1` = LED on
- Value `0` = LED off

### WS2812B (`modbus_tcp_server_ws2812b.py`)

Write holding registers 0-9 to control 10 WS2812B LEDs on GPIO 16:
- Value `1` = green
- Value `2` = red
- Any other value = off

Change `NUM_LEDS` and `PIN_LED` in the script to match your hardware.

</content>