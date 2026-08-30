from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# ============================================================
# SW1 CONNECTION SETTINGS
# ============================================================

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5004,
    "read_timeout_override": 30,
}


# ============================================================
# SW1 TEST COMMANDS ONLY
# ============================================================

test_commands = [

   "ping 192.168.10.1", # sales1 gateway
            "ping 192.168.20.1", # management1 gateway
            "ping  192.168.10.10", # sales1 IP
            "ping 192.168.20.10" # management1 IP

]


# ============================================================
# CONNECT TO SW1
# ============================================================

connection = None

try:

    print("=" * 60)
    print("SW1 NETWORK TESTING")
    print("=" * 60)

    print("\nConnecting to SW1...")

    connection = ConnectHandler(**switch)

    print("SW1 connected successfully.")

    if switch["secret"]:
        connection.enable()

    print("Current prompt:", connection.find_prompt())


    # ========================================================
    # RUN TESTS
    # ========================================================

    for command in test_commands:

        print("\n" + "-" * 60)
        print(f"TEST: {command}")
        print("-" * 60)

        output = connection.send_command_timing(
            command,
            read_timeout=30
        )

        print(output)


    print("\n" + "=" * 60)
    print("SW1 TESTING COMPLETED")
    print("=" * 60)


except NetmikoTimeoutException:

    print("\nConnection timed out.")

except NetmikoAuthenticationException:

    print("\nAuthentication failed.")

except Exception as error:

    print(f"\nUnexpected error: {error}")


finally:

    if connection is not None:
        connection.disconnect()
        print("\nSW1 connection closed.")