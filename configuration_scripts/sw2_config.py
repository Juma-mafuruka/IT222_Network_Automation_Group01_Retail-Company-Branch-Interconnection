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
    "port": 5006,
    "username": "",
    "password": "",
    "secret": "",
    "timeout": 60,
    "conn_timeout": 30,
    "fast_cli": False,
    "global_delay_factor": 2,
}

# ============================================================
# SW2 CONFIGURATION
# ============================================================

commands = [
    # Hostname
    "hostname SW2",

    # --------------------------------------------------------
    # VLAN 10 - SALES
    # --------------------------------------------------------
    "vlan 10",
    "name Sales",
    "exit",

    # --------------------------------------------------------
    # VLAN 20 - MANAGEMENT
    # --------------------------------------------------------
    "vlan 20",
    "name Management",
    "exit",
    
    # ======================================================
            # SW1 SALES IP
            # VLAN 10
            # ======================================================
        
            "interface vlan 10",
            "description SW2_SALES_IP",
            "ip address 192.168.30.2 255.255.255.0",
            "no shutdown",
            "exit",
        
    
        # ======================================================
        # SW1 MANAGEMENT IP
        # VLAN 20
        # ======================================================
    
        "interface vlan 20",
        "description SW2_MANAGEMENT_IP",
        "ip address 192.168.40.2 255.255.255.0",
        "no shutdown",
        "exit",
    
        # ======================================================
        # DEFAULT GATEWAY
        # ======================================================
    
        "ip default-gateway 192.168.40.1",

    # --------------------------------------------------------
    # GIGABITETHERNET0/1 - TRUNK TO R2
    #
    # This switch requires trunk encapsulation to be
    # explicitly set to dot1q before trunk mode.
    # --------------------------------------------------------
    "interface GigabitEthernet0/1",
    "description TRUNK_TO_R2",
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan 10,20",
    "no shutdown",
    "exit",

    # --------------------------------------------------------
    # GIGABITETHERNET0/2 - SALES PC
    # --------------------------------------------------------
    "interface GigabitEthernet0/2",
    "description SALES_PC2",
    "switchport mode access",
    "switchport access vlan 10",
    "spanning-tree portfast",
    "no shutdown",
    "exit",

    # --------------------------------------------------------
    # GIGABITETHERNET0/3 - MANAGEMENT PC
    # --------------------------------------------------------
    "interface GigabitEthernet0/3",
    "description MANAGER_PC2",
    "switchport mode access",
    "switchport access vlan 20",
    "spanning-tree portfast",
    "no shutdown",
    "exit",
]


# ============================================================
# CONNECTION
# ============================================================

connection = None

try:
    print("=" * 60)
    print("CONNECTING TO SW2")
    print("=" * 60)

    connection = ConnectHandler(**switch)

    print("Connected to SW2 successfully.")
    print("Current prompt:", connection.find_prompt())

    # --------------------------------------------------------
    # ENTER ENABLE MODE
    # --------------------------------------------------------

    if not connection.find_prompt().endswith("#"):
        print("Entering privileged EXEC mode...")
        connection.enable()

    print("Privileged prompt:", connection.find_prompt())

    # --------------------------------------------------------
    # CONFIGURE SW2
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONFIGURING SW2")
    print("=" * 60)

    output = connection.send_config_set(
        commands,
        enter_config_mode=True,
        exit_config_mode=True,
    )

    print(output)

    # --------------------------------------------------------
    # SAVE CONFIGURATION
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("SAVING CONFIGURATION")
    print("=" * 60)

    save_output = connection.send_command(
        "write memory",
        expect_string=r"#",
        read_timeout=30,
    )

    print(save_output)

   
    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("SW2 CONFIGURATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:
    print("\nConnection timed out.")
    print(
        "Check the GNS3 VM, SW2 IP address, "
        "and Telnet port 5006."
    )

except NetmikoAuthenticationException:
    print("\nAuthentication failed.")
    print(
        "Check the username, password, "
        "and enable secret."
    )

except Exception as error:
    print("\nUnexpected error:")
    print(error)


# ============================================================
# DISCONNECT
# ============================================================

finally:
    if connection is not None:
        connection.disconnect()
        print("\nDisconnected from SW2.")