# Raspberry Pi Pico W — MicroPython Examples

[![MicroPython](https://img.shields.io/badge/MicroPython-v1.22%2B-blue?logo=micropython)](https://micropython.org/download/RPI_PICO_W/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![YouTube](https://img.shields.io/badge/YouTube-Fusion_Automate-red?logo=youtube)](https://www.youtube.com/channel/UCKKhdFV0q8CV5vWUDfiDfTw)

Collection of **MicroPython** examples for **Raspberry Pi Pico / Pico W** covering WiFi, Modbus TCP/RTU, MQTT, PostgreSQL logging, Telegram bots and Modbus RTU↔TCP gateways. All examples run via [Thonny IDE](https://thonny.org/).

## Table of Contents
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Hardware Requirements](#hardware-requirements)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [1. Basic - WiFi & Sensors](#1-basic---wifi--sensors)
  - [2. Modbus TCP Client](#2-modbus-tcp-client)
  - [3. Modbus TCP Server](#3-modbus-tcp-server)
  - [4. Modbus RTU (RS485) Master](#4-modbus-rtu-rs485-master)
  - [5. MQTT](#5-mqtt)
  - [6. MQTT + Modbus Bridge](#6-mqtt--modbus-bridge)
  - [7. PostgreSQL Logging](#7-postgresql-logging)
  - [8. Telegram](#8-telegram)
  - [9. Gateway - RTU to TCP](#9-gateway---rtu-to-tcp)
- [Firmware](#firmware)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Support](#support)

## Features
- ✅ WiFi connect, Access Point, onboard temperature sensor, LED
- ✅ Modbus TCP **client** (FC 01,02,03,04,05,06,15,16) + **server** with callbacks
- ✅ Modbus RTU master over UART/RS485 (SHT20 etc.)
- ✅ MQTT publish/subscribe (HiveMQ, Mosquitto, Adafruit IO)
- ✅ Modbus → MQTT bridge
- ✅ PostgreSQL cloud logging (`micropg_lite`)
- ✅ Telegram bot (LED/Doorbell)
- ✅ Industrial gateway: RTU ↔ TCP bridge (Pico W WiFi / W5100S-EVB Ethernet)

## Repository Structure
```
RPI-PICO/
├── Basic/                 # WiFi connect, AP, LED, temperature
│   ├── Connect_Pi_Pico_W_to_Wifi.py   # robust helper (see usage below)
│   ├── secrets.example.py             # copy to secrets.py
│   └── ...
├── Modbus/                # TCP client/server + RTU master examples
├── MQTT/                  # Publish/subscribe + Modbus→MQTT
├── PostgreSQL/            # micropg_lite + temp logger
├── Telegram/              # utelegram bot examples
├── Gateway/               # RTU↔TCP gateway (Pico W / W5100S-EVB)
├── Pi-Pico-W-Firmware/    # .uf2 firmware + flash_nuke
└── README.md
```

## Hardware Requirements
- Raspberry Pi Pico **W** (or Pico + W5100S-EVB Pico for Ethernet gateway)
- Micro-USB cable, optional RS485 transceiver (for Modbus RTU), DHT11/SHT20 sensors
- 2.4 GHz WiFi (Pico W does **not** support 5 GHz)

## Quick Start

### 1. Flash MicroPython
Hold `BOOTSEL` → plug USB → drag `.uf2` from `Pi-Pico-W-Firmware/` or download latest:
- Pico: https://micropython.org/download/rp2-pico/
- Pico W: https://micropython.org/download/RPI_PICO_W/
- CircuitPython (alt): https://circuitpython.org/board/raspberry_pi_pico_w/

> To wipe: drag `flash_nuke.uf2` first.

### 2. Install Thonny IDE
Download from https://thonny.org/ → `Tools > Options > Interpreter` → select `MicroPython (Raspberry Pi Pico)`.

### 3. Configure Credentials (Important)
**Never commit secrets.** Each example reads from `secrets.py`:

```bash
# 1. Copy template
copy Basic\secrets.example.py Basic\secrets.py
# 2. Edit Basic/secrets.py
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"
```
All other secrets (MQTT broker, Postgres) follow same pattern — see `secrets.example.py` in each folder.

### 4. Install Libraries (once per board)
In Thonny Shell (`View > Shell`):
```python
import mip
mip.install("github:brainelectronics/micropython-modbus")  # for Modbus/
mip.install("github:mchobby/micropg_lite")                 # for PostgreSQL/ if needed
# umqtt is built-in on recent MicroPython; otherwise:
mip.install("umqtt.simple")
```

### 5. Upload & Run
Open any `.py` in Thonny → `File > Save copy > Raspberry Pi Pico` → Press `Run`.

---

## 📥 Firmware Downloads

| Firmware Type | Download Link |
|---------------|---------------|
| Raspberry Pi Pico MicroPython | [Visit](https://micropython.org/download/rp2-pico/) |
| Raspberry Pi Pico W MicroPython | [Visit](https://micropython.org/download/RPI_PICO_W/) |
| Raspberry Pi Pico W CircuitPython | [Visit](https://circuitpython.org/board/raspberry_pi_pico_w/) |

---

## Usage Guide

### 1. Basic - WiFi & Sensors

| File | What it does | Video |
|------|--------------|-------|
| `Basic/Simple_LED_Blinking.py` | Blink onboard LED | — |
| `Basic/PI_Pico_W_Onboard_Temperature_Sensor.py` | Read internal ADC(4) temp | [Watch](https://youtu.be/7eas25NaM-8) |
| `Basic/Connect_Pi_Pico_W_to_Wifi.py` | **Robust WiFi helper** | — |
| `Basic/Create_Pi_Pico_W_Wifi_AP.py` | Create AP `Pi Pico W AP` | [Watch](https://youtu.be/TQM5PEL98TM) |

#### How to use `Connect_Pi_Pico_W_to_Wifi.py`

```python
# Option A: use secrets.py (recommended)
from Connect_Pi_Pico_W_to_Wifi import connect_wifi
wlan = connect_wifi()  # reads WIFI_SSID/PASSWORD from secrets.py
print(wlan.ifconfig())  # (ip, netmask, gateway, DNS)

# Option B: explicit credentials
wlan = connect_wifi(ssid="MyWiFi", password="secret", timeout=15)

# Helpers
from Connect_Pi_Pico_W_to_Wifi import is_connected, disconnect_wifi
if is_connected(wlan):
    print("online")
```

Features: `timeout` (default 15s), early exit on `WRONG_PASSWORD`/`NO_AP_FOUND`, `retries`, `ValueError` if placeholder not replaced, returns `WLAN` object. Legacy `connect()` → `ip` still works.

Install: `Thonny > File > Save copy > /Basic/secrets.py` on Pico, then `Run`.

---

### 2. Modbus TCP Client

Located in `Modbus/`:

```python
from umodbus.tcp import TCP as ModbusTCPMaster
# WiFi first (see above)
wlan = connect_wifi()

client = ModbusTCPMaster(slave_ip="192.168.1.50", slave_port=502, timeout=5)
regs = client.read_holding_registers(slave_addr=1, starting_addr=0, register_qty=5)
print(regs)
```

| Example | FC | Description | Video |
|---------|----|-------------|-------|
| `Modbus_TCP_Client_Read_HR.py` | 03 | Read holding registers | [Watch](https://youtu.be/goskYrT9-v4) |
| `Modbus_TCP_Client_Write_HR.py` | 06/16 | Write holding registers | [Watch](https://youtu.be/kvvU7n1Poxg) |
| `Modbus_TCP_Client_Read_Coil.py` | 01 | Read coils | [Watch](https://youtu.be/Y8Azq8q3Ax4) |
| `Modbus_TCP_Client_Write_Coil.py` | 05 | Write coil | [Watch](https://youtu.be/UyTNta9OfGE) |
| `Modbus_TCP_Client_Read_IR.py` | 04 | Input registers | [Watch](https://youtu.be/xAi8Ej02De8) |
| `Modbus_TCP_Client_Read_Input_Status.py` | 02 | Discrete inputs | [Watch](https://youtu.be/q0CZX4QeXek) |

> **Note:** Examples previously hardcoded `192.168.29.221` / `Fusion Automate`. Update `secrets.py` or the `slave_ip` variable.

### 3. Modbus TCP Server

```python
from umodbus.tcp import ModbusTCP
import network
wlan = connect_wifi()
server = ModbusTCP()
server.bind(local_ip=wlan.ifconfig()[0], local_port=502)
server.setup_registers(registers={
  "HREGS": {"EXAMPLE_HREG": {"register": 93, "len": 5, "val": 19}},
  "COILS": {"EXAMPLE_COIL": {"register": 123, "len": 1, "val": 1}}
})
while True:
    server.process()
```

- `Modbus/Sample_Modbus_TCP_Server.py` — Full example with callbacks (`on_set_cb`/`on_get_cb`) for Coils/HREGS/ISTS/IREGS.
- `Modbus/Control_LED_Modbus_TCP_Server.py` — Control onboard LED via coil.
- `Modbus/WS2812B_LED_Control_Modbus_TCP_Server_for_Pi_Pico_W_Over_Wifi.py` — WS2812B via Modbus.

Test with `QModMaster` / `ModbusPoll` → connect to `pico_ip:502`.

### 4. Modbus RTU (RS485) Master

Wiring (`Modbus/Pi Pico W  Modbus Serial Connection.png`):
```
Pico W GP0 (TX) → RS485 DI
Pico W GP1 (RX) → RS485 RO
Pico W GP2      → RS485 DE/RE (direction)
GND → GND, 3.3V → VCC
```

```python
from umodbus.serial import Serial as ModbusRTUMaster
rtu = ModbusRTUMaster(uart_id=0, baudrate=9600, pins=(0,1))
regs = rtu.read_holding_registers(slave_addr=1, starting_addr=0, register_qty=2)
```

Examples: `Read Holding/Input Register Values of Modbus Slave Device...py` ([Watch](https://youtu.be/vkr0jXu8t8A), [Watch](https://youtu.be/UVCsmzV5K-Y))

### 5. MQTT

```python
from umqtt.simple import MQTTClient
wlan = connect_wifi()
c = MQTTClient("PicoW", "192.168.1.100", keepalive=30)
c.connect()
c.publish("Pico_W/Sensor/Internal_Temperature", str(25.3))
```

| Example | Broker | Video |
|---------|--------|-------|
| `MQTT/Publish Raspberry Pi Pico W Internal Temperature Data to HiveMQ MQTT Broker.py` | HiveMQ | [Watch](https://youtu.be/4BVE5Q2dj94) |
| `MQTT/MQTT_Publisher_Mosquitto_Broker.py` | Mosquitto LAN | [Watch](https://youtu.be/b3LtdknCkL4) |
| `MQTT/How to Publish DHT11 Sensor Data...py` | Mosquitto + DHT11 | [Watch](https://youtu.be/Gsw0CIsJJfE) |
| `MQTT/MQTT_Pub_Sub_Adafruit_IO.py` | Adafruit IO | — |

Subscribe test: `mosquitto_sub -h 192.168.1.100 -t "Pico_W/#" -v`

### 6. MQTT + Modbus Bridge

`MQTT/Simple_Modbus_to_MQTT_Publisher.py` — reads Modbus holding registers and publishes to MQTT every 1s. Configure at top:
```python
MODBUS_TCP_IP = "192.168.1.50"
MQTT_BROKER = "192.168.1.100"
MQTT_PUBLISH_TOPIC = "Pico_W/Modbus/HR"
```

### 7. PostgreSQL Logging

```python
import micropg_lite
conn = micropg_lite.connect(host="YOUR_PG_HOST", user="user", password="pass", database="mydb")
cur = conn.cursor()
cur.execute("INSERT INTO sensor_data (temperature) VALUES (%s)", (str(temp),))
conn.commit()
```

- Setup table: `CREATE TABLE IF NOT EXISTS sensor_data (id SERIAL PRIMARY KEY, temperature FLOAT NOT NULL, recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);` (see `PostgreSQL/Readme.md:34`)
- Example: `PostgreSQL/RPI_Pico_Internal_temp_to_cloud_PostgreSQL_Data_Logging.py` — logs every 10s. **Update `secrets.py` instead of hardcoded `52.90.199.127`.**

### 8. Telegram

Requires `Telegram/utelegram.py` on Pico (`/lib` or same folder).

```python
# In Telegram/secrets.py
TELEGRAM_BOT_TOKEN = "123:ABC"
WIFI_SSID, WIFI_PASSWORD = "...", "..."
```

- `Pi_Pico_W_Telegram_LED_Control.py` — `/ledon`, `/ledoff`, `/ping`
- `Pi_Pico_W_Telegram_Door_Bell.py`

> Fix: remove `os.chdir('/Raspberry PI Pico W/Telegram')` (`Pi_Pico_W_Telegram_LED_Control.py:4`) — use relative imports.

### 9. Gateway - RTU to TCP

Bridges Modbus RTU (UART) ↔ Modbus TCP (WiFi/Ethernet). See `Gateway/*/README.md`.

```
[SCADA / HMI] --(TCP over WiFi)--> [Pico W Gateway] --(UART/RS485)--> [PLC / Sensor]
```

Quick start (Pico W):
1. Flash `Pi-Pico-W-Firmware/RPI_PICO_W-20240222-v1.22.2.uf2`
2. Copy `Gateway/Modbus Serial to Modbus TCP Gateway using RPI PICO W/Code/*` to Pico
3. Edit `gateway_config.py` → `WIFI_SSID`/`PASSWORD`
4. Run `modbus_rtu_tcp_gateway.py`

Supports FC 01,02,03,04,05,06,15,16.

---

## Firmware

| File | Purpose |
|------|---------|
| `Pi-Pico-W-Firmware/RPI_PICO_W-20251209-v1.27.0.uf2` | Latest (2025-12-09, recommended) |
| `Pi-Pico-W-Firmware/RPI_PICO_W-20240222-v1.22.2.uf2` | Stable |
| `rp2-pico-w-20230405...` | Legacy unstable |
| `flash_nuke.uf2` | Full wipe before reflash |

Flash: hold `BOOTSEL` + plug USB → copy `.uf2` → auto reboot.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Failed to connect status=2` | Wrong password (`secrets.py`) |
| `status=3 NO_AP_FOUND` | SSID typo / 5 GHz AP (use 2.4 GHz) |
| `RuntimeError timeout 15s` | Increase `timeout=30` or check router DHCP |
| `ImportError: no module 'umodbus'` | `mip.install("github:brainelectronics/micropython-modbus")` |
| `os.chdir` not found | Remove hardcoded `os.chdir` in Telegram examples |
| AP `while ap.active == False` hang | Fixed in improved `Create_Pi_Pico_W_Wifi_AP.py` — use `ap.active():` |
| PostgreSQL `connect failed` | Allowlist Pico IP, check port 5432, use `secrets.py` |

## Contributing
PRs welcome. Keep secrets in `secrets.py` (see `secrets.example.py`), use `snake_case` filenames, test on `v1.22+`.

## Support

| Method | Details |
|--------|---------|
| YouTube | [Fusion Automate](https://www.youtube.com/channel/UCKKhdFV0q8CV5vWUDfiDfTw) |
| Telegram | [@fusionautomate](https://t.me/fusionautomate) |
| WhatsApp | [+91-9974477759](https://wa.me/919974477759) |
| Email | [eng.innovativ@gmail.com](mailto:eng.innovativ@gmail.com) |

If useful, ⭐ star the repo and consider [Buy Me a Coffee](https://buymeacoffee.com/pylin).

---
**Fusion Automate - Industrial IoT Solutions**
