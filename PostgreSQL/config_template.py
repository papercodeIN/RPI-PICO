# Configuration Template for Raspberry Pi Pico W Temperature Logger
# Copy this file to config.py and fill in your actual credentials

# Wi-Fi Settings
WIFI_SSID = 'your_wifi_ssid'
WIFI_PASSWORD = 'your_wifi_password'

# PostgreSQL Database Settings
DB_HOST = 'your_server_ip'
DB_USER = 'your_db_username'
DB_PASSWORD = 'your_db_password'
DB_NAME = 'your_db_name'

# Timezone Settings
# IST (Indian Standard Time) is UTC+5:30
TIMEZONE_OFFSET = 19800  # Offset in seconds (5.5 hours * 3600 seconds/hour)
