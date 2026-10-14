# Project Description: Raspberry Pi Pico W Temperature Logger

This project utilizes a **Raspberry Pi Pico W** to continuously monitor and log internal temperature readings into a **PostgreSQL database** over a Wi-Fi connection. The setup involves the following key components and functionalities:

## Key Features

1. **Wi-Fi Connectivity with Auto-Reconnect**: 
   - The Raspberry Pi Pico W connects to a specified Wi-Fi network with automatic retry logic (up to 10 attempts)
   - Automatically detects and reconnects if Wi-Fi connection is lost during operation
   - Provides detailed connection status feedback

2. **Robust PostgreSQL Database Connection**: 
   - Establishes connection to a PostgreSQL database hosted on a remote server
   - Automatic retry logic with 3 attempts and 2-second delays between retries
   - Continuous connection health monitoring and automatic reconnection on failures
   - Graceful error handling with detailed logging

3. **Temperature Reading**: 
   - The internal temperature of the Raspberry Pi Pico W is read using the on-board ADC (Analog-to-Digital Converter)
   - The raw ADC value is converted into a Celsius temperature value using a calibration formula
   - Temperature validation to ensure readings are within the operating range (-20°C to +85°C)
   - Invalid readings are automatically skipped to maintain data quality

4. **Batch Data Logging**: 
   - Temperature readings are collected every 10 seconds
   - Readings are buffered and inserted in batches (default: 6 readings = 1 minute)
   - Batch inserts reduce network overhead and improve reliability
   - Configurable batch size and reading interval
   - Automatic flush of remaining data on program exit

5. **Continuous Monitoring**: 
   - The program runs in an infinite loop, continuously reading the temperature and logging the data
   - Resilient to network interruptions and connection failures
   - Can be manually interrupted by the user (Ctrl+C)

## Compatibility with Other Microcontrollers

This project can also be adapted to work with **ESP32** and **ESP8266** microcontrollers:

- **Wi-Fi Connectivity**: Both the ESP32 and ESP8266 have built-in Wi-Fi capabilities, allowing for similar Wi-Fi connections.
- **Database Connection**: The `micropg_lite` library is compatible with ESP32 and ESP8266, allowing for PostgreSQL database connections.
- **Temperature Reading**: The ESP32 can use its internal sensor, while the ESP8266 can interface with external temperature sensors (e.g., DHT11, DS18B20).

## Setup and Configuration

### 1. Configuration File Setup
Before running the project, you need to configure your credentials:

1. Copy `config_template.py` to `config.py`
2. Edit `config.py` with your actual credentials:
   ```python
   # Wi-Fi Settings
   WIFI_SSID = 'your_wifi_ssid'
   WIFI_PASSWORD = 'your_wifi_password'
   
   # Database Settings
   DB_HOST = 'your_server_ip'
   DB_USER = 'your_db_username'
   DB_PASSWORD = 'your_db_password'
   DB_NAME = 'your_db_name'
   
   # Timezone Settings (IST by default)
   TIMEZONE_OFFSET = 19800  # IST = UTC+5:30 (19800 seconds)
   ```
3. The `config.py` file is excluded from git via `.gitignore` to protect your credentials

**Timezone Configuration:**
- Default is set to IST (Indian Standard Time = UTC+5:30)
- To use other timezones, change `TIMEZONE_OFFSET`:
  - UTC: `TIMEZONE_OFFSET = 0`
  - EST: `TIMEZONE_OFFSET = -18000` (UTC-5:00)
  - PST: `TIMEZONE_OFFSET = -28800` (UTC-8:00)
  - JST: `TIMEZONE_OFFSET = 32400` (UTC+9:00)
- Offset is in seconds: (hours × 3600) + (minutes × 60)

### 2. Database Setup
Create the required table in your PostgreSQL database:

```sql
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Adjustable Parameters
You can modify these settings in the main script:

- `BATCH_SIZE`: Number of readings to batch before inserting (default: 6)
- `READING_INTERVAL`: Seconds between temperature readings (default: 10)
- `NTP_RESYNC_INTERVAL`: Seconds between NTP re-synchronization (default: 3600 = 1 hour)
- Wi-Fi retry attempts: Modify `max_retries` parameter in `connect_wifi()` (default: 10)
- Database retry attempts: Modify `max_retries` parameter in `connect_database()` (default: 3)
- NTP retry attempts: Modify `max_retries` parameter in `sync_time_ntp()` (default: 3)

## Improvements Implemented

### Security Enhancements
✅ **Credentials Externalized** - All sensitive credentials moved to separate `config.py` file that is excluded from version control

### Reliability Improvements
✅ **Wi-Fi Auto-Reconnect** - Automatic retry logic with configurable attempts and timeout  
✅ **Database Auto-Reconnect** - Connection health monitoring with automatic reconnection on failures  
✅ **Temperature Validation** - Invalid readings outside operating range (-20°C to +85°C) are automatically skipped  
✅ **Batch Insert** - Readings are buffered and inserted in batches to reduce network overhead and improve reliability  
✅ **NTP Time Synchronization with IST** - Automatic time sync on startup with IST (UTC+5:30) timezone support, periodic re-sync (hourly), and automatic re-sync after Wi-Fi reconnection

### Code Quality
✅ **Comprehensive Error Handling** - Detailed error messages and graceful degradation on failures  
✅ **Configurable Parameters** - Easy adjustment of batch size, reading intervals, and NTP sync frequency  
✅ **Clean Code Structure** - Well-documented functions with clear separation of concerns

## Suggested Future Enhancements

### Not Yet Implemented
⬜ **Logging Levels** - Add DEBUG flag to reduce console output in production  
⬜ **Data Visualization** - Web dashboard to view temperature trends  
⬜ **Alert System** - Notifications when temperature exceeds thresholds  
⬜ **Additional Sensors** - Support for external DHT11, DS18B20, or other sensors  
⬜ **Local Data Backup** - Store readings locally if database connection fails for extended periods  
⬜ **Health Check Endpoint** - HTTP endpoint to verify device is running properly

## Conclusion

This project serves as a practical example of **IoT (Internet of Things)** data logging, showcasing how microcontrollers can be integrated with cloud-based databases for real-time data monitoring and analysis. The implementation includes production-ready features such as automatic reconnection, batch processing, and data validation, making it suitable for long-term deployment.
