from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# SW2 CONNECTION SETTINGS
# ============================================================

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5006,
    "timeout": 60,
    "conn_timeout": 30,
    "fast_cli": False,
    "global_delay_factor": 2,
}


# ============================================================
# SW2 TESTING COMMANDS
# ============================================================

testing_commands = [

     "ping 192.168.40.1", # management2 gateway
            "ping 192.168.30.1", # sales2 gateway
            "ping 192.168.30.10", # sales2 IP
            "ping 192.168.40.10" # management2 IP

]


# ============================================================
# CONNECT TO SW2
# ============================================================

connection = None

try:

    print("=" * 60)
    print("CONNECTING TO SW2")
    print("=" * 60)

    connection = ConnectHandler(**switch)

    print("SW2 connected successfully.")

    print("Current prompt:", connection.find_prompt())


    # ========================================================
    # ENTER PRIVILEGED EXEC MODE
    # ========================================================

    if not connection.find_prompt().endswith("#"):
        connection.enable()

    print("Privileged prompt:", connection.find_prompt())


    # ========================================================
    # RUN TESTS
    # ========================================================

    for command in testing_commands:

        print("\n" + "=" * 60)
        print(f"TESTING: {command}")
        print("=" * 60)

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)


    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    print("\n" + "=" * 60)
    print("SW2 NETWORK TESTING COMPLETED")
    print("=" * 60)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print("\nConnection timed out.")

    print(
        "Check the GNS3 VM/server IP address, "
        "SW2 TELNET console port, GNS3 VM, "
        "and make sure SW2 is running."
    )


except NetmikoAuthenticationException:

    print("\nAuthentication failed.")

    print(
        "Check the username, password, "
        "and enable password."
    )


except Exception as error:

    print("\nUnexpected error:")
    print(error)


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nSW2 connection closed.")