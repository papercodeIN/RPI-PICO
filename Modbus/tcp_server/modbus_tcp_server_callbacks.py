from umodbus.tcp import ModbusTCP
import time
import network
from secrets import WIFI_SSID, WIFI_PASSWORD, MODBUS_SERVER_PORT

# Connect to WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)
while not station.isconnected():
    time.sleep(1)
print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')

# Use port from secrets configuration
tcp_port = MODBUS_SERVER_PORT
local_ip = station.ifconfig()[0]

# Initialize Modbus TCP server instance
server = ModbusTCP()
is_bound = False

# Bind server to local IP and port if not already bound
is_bound = server.get_bound_status()

if not is_bound:
    server.bind(local_ip=local_ip, local_port=tcp_port)


# Callback triggered when a client writes to EXAMPLE_COIL
def my_coil_set_cb(reg_type, address, val):
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val))


# Callback triggered when a client reads EXAMPLE_COIL
def my_coil_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


# Callback triggered when a client writes to EXAMPLE_HREG
def my_holding_register_set_cb(reg_type, address, val):
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val))


# Callback triggered when a client reads EXAMPLE_HREG
def my_holding_register_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


# Callback triggered when a client reads EXAMPLE_ISTS (discrete inputs are read-only)
def my_discrete_inputs_register_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


# Callback triggered when a client reads EXAMPLE_IREG
# Auto-increments the input register value by 1 before returning it
def my_inputs_register_get_cb(reg_type, address, val):
    global server

    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))

    # Keep operations short to avoid response timeouts
    new_val = val[0] + 1

    server.set_ireg(address=address, value=new_val)
    print('Incremented current value by +1 before sending response')


# Callback triggered when RESET_REGISTER_DATA_COIL is written to
# Restores all registers to their default values defined below
def reset_data_registers_cb(reg_type, address, val):
    global server
    global register_definitions

    print('Resetting register data to default values ...')
    server.setup_registers(registers=register_definitions)
    print('Default values restored')


# Define all exposed registers with their types, addresses, lengths, and default values
# COILS = boolean read/write, HREGS = 16-bit read/write, ISTS = boolean read-only, IREGS = 16-bit read-only
register_definitions = {
    "COILS": {
        "RESET_REGISTER_DATA_COIL": {
            "register": 42,
            "len": 1,
            "val": 0
        },
        "EXAMPLE_COIL": {
            "register": 123,
            "len": 1,
            "val": 1
        }
    },
    "HREGS": {
        "EXAMPLE_HREG": {
            "register": 93,
            "len": 5,
            "val": 19
        }
    },
    "ISTS": {
        "EXAMPLE_ISTS": {
            "register": 67,
            "len": 1,
            "val": 0
        }
    },
    "IREGS": {
        "EXAMPLE_IREG": {
            "register": 10,
            "len": 1,
            "val": 60001
        }
    }
}

# Attach set/get callbacks to coils and holding registers (they support both read and write)
register_definitions['COILS']['EXAMPLE_COIL']['on_set_cb'] = my_coil_set_cb
register_definitions['COILS']['EXAMPLE_COIL']['on_get_cb'] = my_coil_get_cb
register_definitions['HREGS']['EXAMPLE_HREG']['on_set_cb'] = \
    my_holding_register_set_cb
register_definitions['HREGS']['EXAMPLE_HREG']['on_get_cb'] = \
    my_holding_register_get_cb

# Attach get-only callbacks to discrete inputs and input registers (they are read-only)
register_definitions['ISTS']['EXAMPLE_ISTS']['on_get_cb'] = \
    my_discrete_inputs_register_get_cb
register_definitions['IREGS']['EXAMPLE_IREG']['on_get_cb'] = \
    my_inputs_register_get_cb

# Writing coil 42 resets all registers to defaults
register_definitions['COILS']['RESET_REGISTER_DATA_COIL']['on_set_cb'] = \
    reset_data_registers_cb

print('Setting up registers ...')
# Register all defined registers with the Modbus TCP server
server.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as Modbus TCP server on {}:{}'.format(local_ip, tcp_port))

# Main loop: process incoming Modbus TCP requests
while True:
    try:
        result = server.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP server...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as server")
