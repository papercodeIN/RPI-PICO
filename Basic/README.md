# Basic — Pico W Starter Examples

Minimal examples to verify board, WiFi and sensors before using Modbus/MQTT.

## Files
| File | Purpose | Key API |
|------|---------|---------|
| `Simple_LED_Blinking.py` | Blink onboard `LED` | `machine.Pin("LED")` |
| `PI_Pico_W_Onboard_Temperature_Sensor.py` | Read internal temp via `ADC(4)` | `27 - (volt-0.706)/0.001721` |
| `Connect_Pi_Pico_W_to_Wifi.py` | **Robust WiFi helper** — use this for all projects | `connect_wifi()` |
| `Create_Pi_Pico_W_Wifi_AP.py` | Create AP `Pi Pico W AP` | `network.AP_IF` |
| `secrets.example.py` | Template → copy to `secrets.py` (gitignored) | — |

## Quick Start

### 1. Prepare `secrets.py`
```bash
copy secrets.example.py secrets.py
# edit secrets.py:
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"
```
Upload `secrets.py` to Pico via Thonny: `File > Save copy > Raspberry Pi Pico > /Basic/secrets.py` (or root `/secrets.py` — both work via `from secrets import`).

### 2. Test WiFi
Open `Connect_Pi_Pico_W_to_Wifi.py` → `Run`:
```
Connecting to 'YOUR_SSID' (attempt 1/1)...
Connected to 'YOUR_SSID'. Device IP: 192.168.1.42
Network config: ('192.168.1.42', '255.255.255.0', '192.168.1.1', '8.8.8.8')
```
If placeholder error: `ValueError: WiFi credentials not set` → update `secrets.py`.

### 3. Use in your project
```python
from Connect_Pi_Pico_W_to_Wifi import connect_wifi, is_connected
wlan = connect_wifi(timeout=15)  # or connect_wifi("ssid","pass")
assert is_connected(wlan)
# ... your Modbus/MQTT code
```

### API
```python
connect_wifi(ssid=WIFI_SSID, password=WIFI_PASSWORD, timeout=15, retries=1, verbose=True) -> WLAN
is_connected(wlan=None) -> bool
disconnect_wifi() -> None
connect(*args, **kwargs) -> str  # legacy, returns ip
```

Parameters: `timeout` seconds per attempt, `retries` attempts, `verbose` logs. Raises `ValueError` (placeholder) / `RuntimeError` (connect fail).

## Troubleshooting
- `status 2 WRONG_PASSWORD` / `3 NO_AP_FOUND` → check `secrets.py`, 2.4 GHz only.
- `flash_nuke.uf2` if board stuck in boot loop.

## Video Guides
- Thonny install: https://youtu.be/27Tlwy83pqs
- AP mode: https://youtu.be/TQM5PEL98TM
- Internal temp: https://youtu.be/7eas25NaM-8
