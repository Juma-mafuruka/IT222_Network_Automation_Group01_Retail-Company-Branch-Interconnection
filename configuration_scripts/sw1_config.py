from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# ==========================================================
# SW1 CONNECTION DETAILS
# ==========================================================

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",
    "port": 5004,

    "username": "",
    "password": "",
    "secret": "",

    "timeout": 60,
    "conn_timeout": 30,

    "fast_cli": False,
    "global_delay_factor": 2,
}


# ==========================================================
# SW1 CONFIGURATION COMMANDS
# ==========================================================

commands = [
    "hostname SW1",
    # VLAN 10
    "vlan 10",
    "name Sales",
    "exit",

    # VLAN 20
    "vlan 20",
    "name Manager ",
    "exit",
    
     # ======================================================
        # SW1 MANAGEMENT IP
        # VLAN 10
        # ======================================================
    
        "interface vlan 10",
        "description SW1_SALES_IP",
        "ip address 192.168.10.2 255.255.255.0",
        "no shutdown",
        "exit",
        
    
    # ======================================================
    # SW1 MANAGEMENT IP
    # VLAN 20
    # ======================================================

    "interface vlan 20",
    "description SW1_MANAGEMENT_IP",
    "ip address 192.168.20.2 255.255.255.0",
    "no shutdown",
    "exit",

    # ======================================================
    # DEFAULT GATEWAY
    # ======================================================

    "ip default-gateway 192.168.20.1",

    # TRUNK TO R1
    "interface GigabitEthernet0/1",
    "description TRUNK_TO_R1",
    "switchport mode trunk",
    "switchport trunk allowed vlan 10,20",
    "no shutdown",
    "exit",

    # SALES PC
    "interface GigabitEthernet0/2",
    "description SALES_PC1",
    "switchport mode access",
    "switchport access vlan 10",
    "spanning-tree portfast",
    "no shutdown",
    "exit",

    # MANAGEMENT PC
    "interface GigabitEthernet0/3",
    "description MANAGEMENT_PC1",
    "switchport mode access",
    "switchport access vlan 20",
    "spanning-tree portfast",
    "no shutdown",
    "exit",
]


connection = None

try:

    print("Connecting to SW1...")

    connection = ConnectHandler(**switch)

    print("Connected to SW1 successfully.")

    # ======================================================
    # ENABLE MODE
    # ======================================================

    prompt = connection.find_prompt()

    print("Current prompt:", repr(prompt))

    if not prompt.endswith("#"):
        print("Entering enable mode...")
        connection.enable()
        print("Enable prompt:", repr(connection.find_prompt()))

    # ======================================================
    # CONFIGURE SW1
    # ======================================================

    print("\nSending configuration to SW1...")

    output = connection.send_config_set(
        commands,
        enter_config_mode=True,
        exit_config_mode=True
    )

    print(output)

    # ======================================================
    # SAVE CONFIGURATION
    # ======================================================

    print("\nSaving configuration...")

    save_output = connection.save_config()

    print(save_output)

    print("\n========================================")
    print("SW1 CONFIGURATION COMPLETED SUCCESSFULLY")
    print("========================================")


except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check GNS3 VM, IP address and Telnet port."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check username, password and enable secret."
    )


except Exception as error:

    print(f"\nUnexpected error: {error}")


finally: 

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from SW1.")