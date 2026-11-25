<img align="right" src="https://visitor-badge.laobi.icu/badge?page_id=papercodeIN.RPI-PICO" height="20" />

<h1 align="center">🌟 Raspberry Pi Pico W 🌟</h1>

<p align="center">
  <em>MicroPython examples for the Pico W — WiFi, Modbus TCP/RTU, MQTT, PostgreSQL logging, Telegram bots and an RTU-to-TCP gateway</em>
</p>

<p align="center">
  <a href="https://www.youtube.com/@Fusion_Automate"><img src="https://img.shields.io/badge/YouTube-FusionAutomate-%23FF0000?style=for-the-badge&logo=youtube" alt="YouTube"></a>
  <a href="https://www.instagram.com/fusion_automate"><img src="https://img.shields.io/badge/Instagram-fusion__automate-%23E4405F?style=for-the-badge&logo=instagram" alt="Instagram"></a>
  <a href="https://x.com/fusion_automate"><img src="https://img.shields.io/badge/X-fusion__automate-000000?style=for-the-badge&logo=x" alt="X (Twitter)"></a>
  <a href="https://t.me/fusionautomate"><img src="https://img.shields.io/badge/Telegram-%40fusionautomate-%2326A5E4?style=for-the-badge&logo=telegram" alt="Telegram"></a>
  <a href="https://fusionautomate.in/"><img src="https://img.shields.io/badge/Website-fusionautomate.in-blueviolet?style=for-the-badge" alt="Website"></a>
</p>

[![MicroPython](https://img.shields.io/badge/MicroPython-v1.22%2B-blue?logo=micropython)](https://micropython.org/download/RPI_PICO_W/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Lessons](https://img.shields.io/badge/Training_Lessons-25-FF9800)](#-training-index)
[![Videos](https://img.shields.io/badge/Training_Videos-16-9C27B0)](#-training-index)

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
├── Modbus/                # TCP client/server + RTU master examples
├── MQTT/                  # Publish/subscribe + Modbus→MQTT
├── PostgreSQL/            # micropg_lite + temp logger
├── Telegram/              # utelegram bot examples
├── Gateway/               # RTU↔TCP gateway (Pico W / W5100S-EVB)
├── Pi-Pico-W-Firmware/    # .uf2 firmware + flash_nuke
└── README.md
```

Each folder has a `secrets.example.py` — copy it to `secrets.py` and fill in your credentials. **Never commit secrets.**

## Hardware Requirements

- Raspberry Pi Pico **W** (or Pico + W5100S-EVB Pico for the Ethernet gateway)
- Micro-USB cable, optional RS485 transceiver (Modbus RTU), DHT11/SHT20 sensors
- 2.4 GHz WiFi (Pico W does **not** support 5 GHz)

## Quick Start

1. **Flash MicroPython** — hold `BOOTSEL`, plug USB, drag a `.uf2` from `Pi-Pico-W-Firmware/` (drag `flash_nuke.uf2` first to wipe).
2. **Install Thonny IDE** — <https://thonny.org> → `Tools > Options > Interpreter` → select `MicroPython (Raspberry Pi Pico)`.
3. **Configure credentials** — copy each folder's `secrets.example.py` to `secrets.py` and set `WIFI_SSID` / `WIFI_PASSWORD`.
4. **Install libraries** (once per board, in the Thonny shell):
   ```python
   import mip
   mip.install("github:brainelectronics/micropython-modbus")  # Modbus/
   mip.install("github:mchobby/micropg_lite")                 # PostgreSQL/ if needed
   ```
   `umqtt` is built-in on recent MicroPython.
5. **Run** — open any `.py` in Thonny → `File > Save copy > Raspberry Pi Pico` → press `Run`.

## Firmware

| File | Purpose |
|------|---------|
| `Pi-Pico-W-Firmware/RPI_PICO_W-20251209-v1.27.0.uf2` | Latest MicroPython (recommended) |
| `Pi-Pico-W-Firmware/RPI_PICO_W-20240222-v1.22.2.uf2` | Stable |
| `flash_nuke.uf2` | Full wipe before reflash |

Downloads: [Pico MicroPython](https://micropython.org/download/rp2-pico/) · [Pico W MicroPython](https://micropython.org/download/RPI_PICO_W/) · [CircuitPython (alt)](https://circuitpython.org/board/raspberry_pi_pico_w/)

## Usage Guide

### 1. Basic — WiFi & Sensors

| File | What it does |
|------|--------------|
| `Basic/Simple_LED_Blinking.py` | Blink onboard LED |
| `Basic/PI_Pico_W_Onboard_Temperature_Sensor.py` | Read internal ADC(4) temperature |
| `Basic/Connect_Pi_Pico_W_to_Wifi.py` | **Robust WiFi helper** |
| `Basic/Create_Pi_Pico_W_Wifi_AP.py` | Create WiFi Access Point |

```python
from Connect_Pi_Pico_W_to_Wifi import connect_wifi
wlan = connect_wifi()                                  # uses secrets.py
wlan = connect_wifi(ssid="MyWiFi", password="secret")  # or explicit
```
Features: `timeout` (default 15s), early exit on `WRONG_PASSWORD` / `NO_AP_FOUND`, `retries`, returns a `WLAN` object. Helpers: `is_connected(wlan)`, `disconnect_wifi(wlan)`.

### 2. Modbus TCP Client

```python
from umodbus.tcp import TCP as ModbusTCPMaster
wlan = connect_wifi()   # WiFi first

client = ModbusTCPMaster(slave_ip="192.168.1.50", slave_port=502, timeout=5)
regs = client.read_holding_registers(slave_addr=1, starting_addr=0, register_qty=5)
```

| Example | FC | Description |
|---------|----|-------------|
| `Modbus_TCP_Client_Read_HR.py` | 03 | Read holding registers |
| `Modbus_TCP_Client_Write_HR.py` | 06/16 | Write holding registers |
| `Modbus_TCP_Client_Read_Coil.py` | 01 | Read coils |
| `Modbus_TCP_Client_Write_Coil.py` | 05 | Write coil |
| `Modbus_TCP_Client_Read_IR.py` | 04 | Read input registers |
| `Modbus_TCP_Client_Read_Input_Status.py` | 02 | Read discrete inputs |

> **Note:** older examples hardcoded `192.168.29.221` — set `slave_ip` or `secrets.py` yourself.

### 3. Modbus TCP Server

```python
from umodbus.tcp import ModbusTCP
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

- `Modbus/Sample_Modbus_TCP_Server.py` — full example with `on_set_cb` / `on_get_cb` callbacks
- `Modbus/Control_LED_Modbus_TCP_Server.py` — control onboard LED via coil
- `Modbus/WS2812B_LED_Control_Modbus_TCP_Server_for_Pi_Pico_W_Over_Wifi.py` — WS2812B over Modbus

Test with `QModMaster` / `ModbusPoll` → connect to `<pico_ip>:502`.

### 4. Modbus RTU (RS485) Master

Wiring (`Modbus/Pi Pico W  Modbus Serial Connection.png`):
```
Pico W GP0 (TX) → RS485 DI
Pico W GP1 (RX) → RS485 RO
Pico W GP2      → RS485 DE/RE
GND → GND, 3.3V → VCC
```

```python
from umodbus.serial import Serial as ModbusRTUMaster
rtu = ModbusRTUMaster(uart_id=0, baudrate=9600, pins=(0,1))
regs = rtu.read_holding_registers(slave_addr=1, starting_addr=0, register_qty=2)
```

### 5. MQTT

```python
from umqtt.simple import MQTTClient
wlan = connect_wifi()
c = MQTTClient("PicoW", "192.168.1.100", keepalive=30)
c.connect()
c.publish("Pico_W/Sensor/Internal_Temperature", str(25.3))
```

| Example | Broker |
|---------|--------|
| `MQTT/Publish Raspberry Pi Pico W Internal Temperature Data to HiveMQ MQTT Broker.py` | HiveMQ |
| `MQTT/MQTT_Publisher_Mosquitto_Broker.py` | Mosquitto (LAN) |
| `MQTT/How to Publish DHT11 Sensor Data...py` | Mosquitto + DHT11 |
| `MQTT/MQTT_Pub_Sub_Adafruit_IO.py` | Adafruit IO |

Subscribe test: `mosquitto_sub -h 192.168.1.100 -t "Pico_W/#" -v`

### 6. MQTT + Modbus Bridge

`MQTT/Simple_Modbus_to_MQTT_Publisher.py` — reads Modbus holding registers and publishes to MQTT every 1 s. Configure at the top:

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

- Table setup: see `PostgreSQL/Readme.md`
- `PostgreSQL/RPI_Pico_Internal_temp_to_cloud_PostgreSQL_Data_Logging.py` — logs every 10 s

### 8. Telegram

Put `Telegram/utelegram.py` on the Pico (`/lib` or same folder) and set `TELEGRAM_BOT_TOKEN` in `Telegram/secrets.py`.

- `Pi_Pico_W_Telegram_LED_Control.py` — `/ledon`, `/ledoff`, `/ping`
- `Pi_Pico_W_Telegram_Door_Bell.py`

> Fix: remove the hardcoded `os.chdir(...)` line in `Pi_Pico_W_Telegram_LED_Control.py` — use relative imports.

### 9. Gateway — RTU to TCP

Bridges Modbus RTU (UART) ↔ Modbus TCP (WiFi / Ethernet). Details in `Gateway/*/README.md`.

```
[SCADA / HMI] --(TCP over WiFi)--> [Pico W Gateway] --(UART/RS485)--> [PLC / Sensor]
```

Quick start (Pico W): copy `Gateway/Modbus Serial to Modbus TCP Gateway using RPI PICO W/Code/*` to the board → edit `gateway_config.py` → run `modbus_rtu_tcp_gateway.py`. Supports FC 01,02,03,04,05,06,15,16.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Failed to connect status=2` | Wrong password (`secrets.py`) |
| `status=3 NO_AP_FOUND` | SSID typo / 5 GHz AP (use 2.4 GHz) |
| `RuntimeError timeout 15s` | Increase `timeout=30` or check router DHCP |
| `ImportError: no module 'umodbus'` | `mip.install("github:brainelectronics/micropython-modbus")` |
| `os.chdir` not found | Remove the hardcoded `os.chdir` in Telegram examples |
| AP `while ap.active == False` hang | Use `ap.active():` (fixed in improved example) |
| PostgreSQL `connect failed` | Allowlist the Pico IP, check port 5432, use `secrets.py` |

## Contributing

PRs welcome. Keep secrets in `secrets.py`, use `snake_case` filenames, test on MicroPython `v1.22+`.

## Contact

| Method | Details |
|--------|---------|
| Call / WhatsApp | [+91-9974477759](https://wa.me/919974477759) |
| Telegram | [@fusionautomate](https://t.me/fusionautomate) |
| Email | [eng.innovativ@gmail.com](mailto:eng.innovativ@gmail.com) |

---

# 🎓 Training Index

*Step-by-step video lessons for this repository — follow them in order.*

**Legend:** 🆓 Free lesson · ✅ Video available · ⌛ In progress / coming soon

> 📦 **Note:** The 📦 **Code** column is reserved for the lesson source code — code links will be added here as each example becomes available.

## 📘 Module 1 · Basic

| # | Lesson | Watch |
|:-:|--------|:-----:|
| 1 | 🆓 Install Thonny IDE on Windows | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/27Tlwy83pqs) |
| 2 | 🆓 Connect Pico W to Wi-Fi | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/22UFBnDFj1o) |
| 3 | 🆓 Install Modbus Library (MicroPython) | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/BXMauNF7mpU) |
| 4 | 🆓 Create Wi-Fi Access Point | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/TQM5PEL98TM) |
| 5 | 🆓 Read Internal Temperature Sensor | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/7eas25NaM-8) |

## 📘 Module 2 · Modbus TCP/IP Client

| # | Lesson | Watch | 📦 Code |
|:-:|--------|:-----:|:-------:|
| 1 | 🆓 Read Holding Registers | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/goskYrT9-v4) | ⌛ |
| 2 | 🆓 Write Holding Registers | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/kvvU7n1Poxg) | ⌛ |
| 3 | 🆓 Read Coil Status | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/Y8Azq8q3Ax4) | ⌛ |
| 4 | 🆓 Write / Update Coil Status | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/UyTNta9OfGE) | ⌛ |
| 5 | 🆓 Read Input Registers | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/xAi8Ej02De8) | ⌛ |
| 6 | 🆓 Read Discrete Input Status | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/q0CZX4QeXek) | ⌛ |
| 7 | 🆓 Control Digital Pins via Modbus TCP | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/vA3utOAW49Y) | ⌛ |

## 📘 Module 3 · Modbus TCP/IP Server

| # | Lesson | Watch | 📦 Code |
|:-:|--------|:-----:|:-------:|
| 1 | Create Simple Modbus TCP/IP Server (Coils · Inputs · Registers) | ⌛ | ⌛ |
| 2 | Communication with SHT20 Modbus Serial Transmitter | ⌛ | ⌛ |

## 📘 Module 4 · MQTT

| # | Lesson | Watch | 📦 Code |
|:-:|--------|:-----:|:-------:|
| 1 | Publish Internal Temperature to HiveMQ | ⌛ | ⌛ |
| 2 | 🆓 Monitor Internal Temperature via Mosquitto (LAN) | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/b3LtdknCkL4) | ⌛ |
| 3 | 🆓 Publish DHT11 Data to Mosquitto (LAN) | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/Gsw0CIsJJfE) | ⌛ |

## 📘 Module 5 · MQTT + Modbus TCP/IP Client

| # | Lesson | Watch | 📦 Code |
|:-:|--------|:-----:|:-------:|
| 1 | Read Holding Registers → Publish to MQTT | ⌛ | ⌛ |
| 2 | Read Multiple Modbus TCP Devices → Publish to MQTT | ⌛ | ⌛ |

## 📘 Module 6 · Modbus Serial (RS485) Master

| # | Lesson | Watch | 📦 Code |
|:-:|--------|:-----:|:-------:|
| 1 | 🆓 Read Holding Registers of Modbus Slave | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/vkr0jXu8t8A) | ⌛ |
| 2 | 🆓 Read Input Registers of Modbus Slave | [![Watch](https://img.shields.io/badge/▶_Watch-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/UVCsmzV5K-Y) | ⌛ |
| 3 | Read Coil Status of Modbus Slave | ⌛ | ⌛ |
| 4 | Read Input Coil Status of Modbus Slave | ⌛ | ⌛ |
| 5 | Write Holding Registers to Modbus Slave | ⌛ | ⌛ |
| 6 | Change Coil Status of Modbus Slave | ⌛ | ⌛ |

---

<div align="center">

✨ **Enjoying these lessons? Support our work!** ✨

<a href="https://buymeacoffee.com/pylin" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" height="40">
</a>

<a href="https://www.youtube.com/channel/UCKKhdFV0q8CV5vWUDfiDfTw" target="_blank">
  <img src="https://raw.githubusercontent.com/papercodeIN/RPI-PICO/main/assets/youtube-subscribe.png" alt="Subscribe on YouTube" height="40">
</a>

<p>⭐ Star this repo if it helped you · <strong>Fusion Automate — Industrial IoT Solutions</strong></p>

</div>
