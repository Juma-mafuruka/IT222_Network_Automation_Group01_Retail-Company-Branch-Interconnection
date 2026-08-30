from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# ============================================================
# SW2 - RETAIL COMPANY NETWORK VERIFICATION
# ============================================================

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",   # GNS3 VM IP address
    "username": "",
    "password": "",
    "secret": "",
    "port": 5004,
    "read_timeout_override": 30,
}


# ============================================================
# VERIFICATION COMMANDS
# ============================================================

verification_commands = [

    # 1. Verify VLAN 10 and VLAN 20
    "show vlan brief",

    # 2. Verify interface status
    "show interfaces status",

    # 3. Verify trunk configuration
    "show interfaces trunk",

    # 4. Verify required interface configurations
    "show run interface Gi0/1",
    "show run interface Gi0/2",
    "show run interface Gi0/3",

    # 5. Verify learned MAC addresses
    "show mac address-table",

    # 6. Verify neighboring Cisco devices
    "show cdp neighbors",

    # 7. Verify detailed CDP information
    "show cdp neighbors detail",
]


connection = None

try:

    # ========================================================
    # CONNECT TO SW2
    # ========================================================

    print("=" * 70)
    print("SW2 RETAIL NETWORK VERIFICATION")
    print("=" * 70)

    print("\nConnecting to SW2...")

    connection = ConnectHandler(**switch)

    print("Connected to SW2 successfully.")

    # ========================================================
    # ENTER ENABLE MODE
    # ========================================================

    if switch["secret"]:
        print("Entering enable mode...")
        connection.enable()

    print(f"Current prompt: {connection.find_prompt()}")

    # ========================================================
    # RUN VERIFICATION COMMANDS
    # ========================================================

    for command in verification_commands:

        print("\n" + "-" * 70)
        print(f"COMMAND: {command}")
        print("-" * 70)

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)

    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n" + "=" * 70)
    print("SW2 VERIFICATION COMPLETED SUCCESSFULLY")
    print("=" * 70)


except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check the GNS3 VM IP address, SW2 TELNET console port, "
        "GNS3 VM, and SW2 state."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(f"\nUnexpected error: {error}")


finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from SW2.")