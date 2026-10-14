import network  # Handles the Wi-Fi connection
import micropg_lite
import machine
import time
import config  # Import configuration file

try:
    import ntptime  # For NTP time synchronization
except ImportError:
    ntptime = None
    print("Warning: ntptime module not available. Time synchronization will be skipped.")

# Function to synchronize time with NTP server and apply timezone offset
def sync_time_ntp(max_retries=3):
    """
    Synchronize device time with NTP server and apply timezone offset for IST.
    
    Args:
        max_retries: Maximum number of synchronization attempts
    
    Returns:
        True if successful, False otherwise
    """
    if ntptime is None:
        print("NTP module not available. Skipping time synchronization.")
        return False
    
    for attempt in range(max_retries):
        try:
            print(f"Synchronizing time with NTP server (attempt {attempt + 1}/{max_retries})...")
            
            # Sync time with NTP server (sets UTC time)
            ntptime.settime()
            
            # Apply timezone offset for IST if configured
            if hasattr(config, 'TIMEZONE_OFFSET') and config.TIMEZONE_OFFSET != 0:
                # Get the RTC object
                rtc = machine.RTC()
                
                # Get current UTC time
                utc_seconds = time.time()
                
                # Add timezone offset to get local time
                local_seconds = utc_seconds + config.TIMEZONE_OFFSET
                
                # Convert to time tuple
                local_time = time.gmtime(local_seconds)
                
                # Set RTC with local time: (year, month, day, weekday, hour, minute, second, subseconds)
                # weekday: 0 = Monday, 6 = Sunday
                rtc.datetime((local_time[0], local_time[1], local_time[2], local_time[6], 
                             local_time[3], local_time[4], local_time[5], 0))
                
                # Display synchronized time in IST
                current_time = time.localtime()
                print(f"Time synchronized successfully (IST): {current_time[0]}-{current_time[1]:02d}-{current_time[2]:02d} {current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}")
                print(f"Timezone: IST (UTC+{config.TIMEZONE_OFFSET/3600:.1f})")
            else:
                # No timezone offset configured, show UTC
                current_time = time.localtime()
                print(f"Time synchronized successfully (UTC): {current_time[0]}-{current_time[1]:02d}-{current_time[2]:02d} {current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}")
            
            return True
        except Exception as e:
            print(f"NTP sync failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    print("Warning: Unable to synchronize time with NTP server. Timestamps may be inaccurate.")
    return False

# Function to connect to Wi-Fi with retry logic
def connect_wifi(ssid, password, max_retries=10, timeout=1):
    """
    Connect to Wi-Fi with retry logic and timeout.
    
    Args:
        ssid: Wi-Fi network name
        password: Wi-Fi password
        max_retries: Maximum number of connection attempts
        timeout: Time to wait between retries in seconds
    
    Returns:
        wlan object if successful, None if failed
    """
    print("Connecting to Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    retry_count = 0
    while not wlan.isconnected() and retry_count < max_retries:
        time.sleep(timeout)
        retry_count += 1
        print(f"Retry {retry_count}/{max_retries}...")
    
    if wlan.isconnected():
        print("Wi-Fi connected:", wlan.ifconfig())
        return wlan
    else:
        print("Failed to connect to Wi-Fi after", max_retries, "attempts")
        return None

# Function to connect to PostgreSQL database
def connect_database(host, user, password, database, max_retries=3):
    """
    Connect to PostgreSQL database with retry logic.
    
    Args:
        host: Database server IP/hostname
        user: Database username
        password: Database password
        database: Database name
        max_retries: Maximum number of connection attempts
    
    Returns:
        connection object if successful, None if failed
    """
    for attempt in range(max_retries):
        try:
            print(f"Connecting to PostgreSQL database (attempt {attempt + 1}/{max_retries})...")
            conn = micropg_lite.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Database connection successful.")
            return conn
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{max_retries}):", e)
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Unable to connect to database after", max_retries, "attempts")
                return None

# Connect to Wi-Fi
wlan = connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
if not wlan:
    raise Exception("Failed to establish Wi-Fi connection")

# Synchronize time with NTP server
print("\n--- Time Synchronization ---")
sync_time_ntp()
print("--- Time Synchronization Complete ---\n")

# Connect to PostgreSQL
conn = connect_database(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
if not conn:
    raise Exception("Failed to establish database connection")

cur = conn.cursor()

# Configuration for batch inserts
BATCH_SIZE = 6  # Number of readings to batch before inserting (6 readings = 1 minute)
READING_INTERVAL = 10  # Seconds between each temperature reading
NTP_RESYNC_INTERVAL = 3600  # Re-sync time every hour (3600 seconds)

# Track last NTP sync time
last_ntp_sync = time.time()

# Function to read internal temperature
def read_internal_temperature():
    print("Reading internal temperature...")
    adc = machine.ADC(4)  # Internal temperature sensor is usually on GPIO 4
    raw_value = adc.read_u16()  # Read raw value (0-65535)
    
    # Convert raw value to temperature in Celsius
    temperature = (raw_value / 65535) * 3.3  # Convert to voltage (0 to 3.3V)
    temperature = (temperature - 0.5) * 100  # Convert to Celsius (0.5V corresponds to 0°C)
    
    print(f"Raw value: {raw_value}, Temperature: {temperature:.2f}°C")
    return round(temperature, 2)

# Function to validate temperature reading
def is_valid_temperature(temperature):
    """
    Validate if temperature is within reasonable range for Pico W.
    Operating range: -20°C to +85°C
    
    Args:
        temperature: Temperature value in Celsius
    
    Returns:
        True if valid, False otherwise
    """
    return -20 <= temperature <= 85

# Function to insert batch data into database
def insert_batch_data(cursor, connection, batch):
    """
    Insert multiple temperature readings in a single SQL statement.
    
    Args:
        cursor: Database cursor
        connection: Database connection
        batch: List of temperature readings
    
    Returns:
        True if successful, False otherwise
    """
    if not batch:
        return True
    
    try:
        # Build VALUES clause: (temp1), (temp2), (temp3), ...
        values_list = ', '.join([f"({str(temp)})" for temp in batch])
        query = f"INSERT INTO sensor_data (temperature) VALUES {values_list}"
        
        print(f"Inserting batch of {len(batch)} readings into database...")
        cursor.execute(query)
        connection.commit()
        print(f"Successfully inserted {len(batch)} temperature readings")
        return True
    except Exception as e:
        print(f"Error inserting batch data: {e}")
        return False

# Loop to collect and batch insert temperature data
temperature_batch = []  # Buffer to store readings before batch insert

try:
    while True:
        # Record the start time of the loop
        start_time = time.time()
        
        # Check if it's time to re-sync with NTP server
        if time.time() - last_ntp_sync >= NTP_RESYNC_INTERVAL:
            print("\n--- Periodic NTP Re-synchronization ---")
            if sync_time_ntp():
                last_ntp_sync = time.time()
            print("--- Re-synchronization Complete ---\n")
        
        # Check Wi-Fi connection and reconnect if necessary
        if not wlan.isconnected():
            print("Wi-Fi connection lost. Reconnecting...")
            wlan = connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
            if not wlan:
                print(f"Failed to reconnect to Wi-Fi. Retrying in {READING_INTERVAL} seconds...")
                time.sleep(READING_INTERVAL)
                continue
            # Re-sync time after Wi-Fi reconnection
            sync_time_ntp()
            last_ntp_sync = time.time()
        
        # Check database connection and reconnect if necessary
        if not conn or not conn.is_connect():
            print("Database connection lost. Reconnecting...")
            conn = connect_database(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            if not conn:
                print(f"Failed to reconnect to database. Retrying in {READING_INTERVAL} seconds...")
                time.sleep(READING_INTERVAL)
                continue
            cur = conn.cursor()
        
        # Read internal temperature
        temperature = read_internal_temperature()
        
        # Validate temperature reading
        if not is_valid_temperature(temperature):
            print(f"Invalid temperature reading: {temperature}°C (outside -20°C to +85°C range). Skipping...")
            # Calculate sleep time and wait for next iteration
            elapsed_time = time.time() - start_time
            sleep_time = READING_INTERVAL - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
            continue
        
        # Add temperature to batch
        temperature_batch.append(temperature)
        print(f"Added temperature {temperature:.2f}°C to batch (batch size: {len(temperature_batch)}/{BATCH_SIZE})")
        
        # Insert batch when it reaches the configured size
        if len(temperature_batch) >= BATCH_SIZE:
            success = insert_batch_data(cur, conn, temperature_batch)
            
            if success:
                # Clear the batch after successful insert
                temperature_batch.clear()
            else:
                # If insert failed, mark connection as potentially invalid
                print("Batch insert failed. Will retry on next batch.")
                # Keep the batch data for next attempt, but limit growth
                if len(temperature_batch) > BATCH_SIZE * 3:
                    print(f"Warning: Batch size exceeded {BATCH_SIZE * 3}. Discarding oldest readings.")
                    temperature_batch = temperature_batch[-BATCH_SIZE:]

        # Calculate how long the operations took
        elapsed_time = time.time() - start_time

        # Sleep for the remaining time to ensure the loop runs at the configured interval
        sleep_time = READING_INTERVAL - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Program stopped by user.")
    # Insert any remaining data in batch before exiting
    if temperature_batch:
        print(f"Inserting remaining {len(temperature_batch)} readings before exit...")
        insert_batch_data(cur, conn, temperature_batch)
finally:
    if conn and conn.is_connect():
        conn.close()
    print("Connection closed.")

