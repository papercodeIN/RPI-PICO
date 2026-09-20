# Pi Pico W WiFi Connection Script
# Description: Robust WiFi connection helper for Raspberry Pi Pico W (MicroPython)
# Firmware: MicroPython v1.22+ for RP2 Pico W
# Usage: copy secrets.example.py -> secrets.py and fill your credentials

import time
import network
import machine

# Try to load credentials from secrets.py, fall back to placeholders
try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
except ImportError:
    WIFI_SSID = "YOUR_SSID"
    WIFI_PASSWORD = "YOUR_PASSWORD"
    print("Warning: secrets.py not found, using placeholder credentials.")
    print("Copy Basic/secrets.example.py to Basic/secrets.py and update it.")


def connect_wifi(
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    timeout=15,
    retries=1,
    verbose=True,
):
    """
    Connect Raspberry Pi Pico W to WiFi with timeout and status handling.

    Args:
        ssid (str): WiFi SSID
        password (str): WiFi password
        timeout (int): seconds to wait per attempt
        retries (int): number of connection attempts
        verbose (bool): print status messages

    Returns:
        network.WLAN: connected WLAN instance

    Raises:
        RuntimeError: if connection fails after retries
        ValueError: if ssid/password are placeholders or empty
    """
    if not ssid or ssid == "YOUR_SSID" or not password or password == "YOUR_PASSWORD":
        raise ValueError(
            "WiFi credentials not set. Update secrets.py (see secrets.example.py)"
        )

    wlan = network.WLAN(network.STA_IF)

    # Clean previous state if needed
    if wlan.active() and wlan.isconnected():
        if verbose:
            print(f"Already connected, disconnecting from {wlan.config('essid')}")
        wlan.disconnect()
        time.sleep(1)

    wlan.active(True)
    # Optional: set hostname and power management for better stability
    # wlan.config(hostname="pico-w")

    last_status = None
    for attempt in range(1, retries + 1):
        if verbose:
            print(f"Connecting to '{ssid}' (attempt {attempt}/{retries})...")

        # MicroPython status codes:
        # STAT_IDLE=0, STAT_CONNECTING=1, STAT_WRONG_PASSWORD=2,
        # STAT_NO_AP_FOUND=3, STAT_CONNECT_FAIL=4, STAT_GOT_IP=3 (varies by port)
        wlan.connect(ssid, password)

        for _ in range(timeout):
            status = wlan.status()
            if status != last_status and verbose:
                # Provide human-readable status on change
                status_text = {
                    0: "STAT_IDLE",
                    1: "STAT_CONNECTING",
                    2: "STAT_WRONG_PASSWORD",
                    3: "STAT_GOT_IP / STAT_NO_AP_FOUND",
                    4: "STAT_CONNECT_FAIL",
                }.get(status, str(status))
                # Uncomment for debugging: print(f"  status: {status_text}")
                last_status = status

            if wlan.isconnected():
                ip = wlan.ifconfig()[0]
                if verbose:
                    print(f"Connected to '{ssid}'. Device IP: {ip}")
                return wlan

            # Early exit on unrecoverable errors
            if status in (network.STAT_WRONG_PASSWORD, network.STAT_NO_AP_FOUND):
                if verbose:
                    print(f"WiFi failed quickly with status {status}")
                break

            time.sleep(1)

        if wlan.isconnected():
            break

        if verbose:
            print(f"Attempt {attempt} failed (status={wlan.status()}).")

        if attempt < retries:
            wlan.disconnect()
            time.sleep(2)

    # Final failure cleanup
    status = wlan.status()
    wlan.active(False)
    raise RuntimeError(
        f"Failed to connect to '{ssid}' after {retries} attempt(s). "
        f"Last status={status}. Check SSID/password and 2.4GHz availability."
    )


def is_connected(wlan=None):
    """Check if WLAN is connected."""
    if wlan is None:
        wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()


def disconnect_wifi():
    """Gracefully disconnect and power down WLAN."""
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(0.5)
    wlan.active(False)
    print("WiFi disconnected.")

# Legacy alias for backward compatibility
def connect(*args, **kwargs):
    """Legacy alias for connect_wifi(). Prefer connect_wifi()."""
    wlan = connect_wifi(*args, **kwargs)
    return wlan.ifconfig()[0]


if __name__ == "__main__":
    try:
        wlan = connect_wifi()
        # Keep connection alive - replace with your main logic
        # Example: print network config
        print("Network config:", wlan.ifconfig())
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        disconnect_wifi()
        # Do not hard-reset; allow clean exit for Thonny REPL
