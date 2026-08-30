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
}


verification_commands = [
    "show version",
    "show vlan brief",
    "show ip interface brief",
    "show interfaces trunk",
    "show interfaces status",
    "show run interface Gi0/1",
    "show run interface Gi0/2",
    "show run interface Gi0/3",

]


# ============================================================
# CONNECT TO SW2
# ============================================================

connection = None

try:

    print("=" * 60)
    print("SW2 NETWORK VERIFICATION")
    print("=" * 60)

    print("\nConnecting to SW2...")

    connection = ConnectHandler(**switch)

    print("Connected successfully.")

    print("Current prompt:", connection.find_prompt())


    # ========================================================
    # ENTER PRIVILEGED EXEC MODE
    # ========================================================

    if not connection.find_prompt().endswith("#"):
        connection.enable()

    print("Privileged prompt:", connection.find_prompt())


    # ========================================================
    # RUN VERIFICATION COMMANDS
    # ========================================================

    for command in verification_commands:

        print("\n" + "=" * 60)
        print(f"VERIFYING: {command}")
        print("=" * 60)

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)


    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n" + "=" * 60)
    print("SW2 VERIFICATION COMPLETED SUCCESSFULLY")
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