from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# ============================================================
# R1 CONNECTION DETAILS
# ============================================================

router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5000,
    "read_timeout_override": 30,
}


# ============================================================
# R1 CONFIGURATION
# ============================================================

commands = [

    # Hostname
    "hostname R1",

    # ========================================================
    # TRUNK TO SW1
    # ========================================================

    "interface gigabitEthernet0/0",
    "description TRUNK_TO_SW1",
    "no ip address",
    "no shutdown",
    "exit",

    # ========================================================
    # VLAN 10 - SALES
    # ========================================================

    "interface gigabitEthernet0/0.10",
    "description SALES_VLAN_10",
    "encapsulation dot1Q 10",
    "ip address 192.168.10.1 255.255.255.0",
    "no shutdown",
    "exit",

    # ========================================================
    # VLAN 20 - MANAGEMENT
    # ========================================================

    "interface gigabitEthernet0/0.20",
    "description MANAGEMENT_VLAN_20",
    "encapsulation dot1Q 20",
    "ip address 192.168.20.1 255.255.255.0",
    "no shutdown",
    "exit",

    # ========================================================
    # LINK TO R2
    # ========================================================

    "interface gigabitEthernet0/1",
    "description LINK_TO_R2",
    "ip address 10.1.1.1 255.255.255.252",
    "no shutdown",
    "exit",

    # ========================================================
    # STATIC ROUTES TO R2 NETWORKS
    # ========================================================

    "ip route 192.168.30.0 255.255.255.0 10.1.1.2",
    "ip route 192.168.40.0 255.255.255.0 10.1.1.2",
]


def main():

    connection = None

    try:

        print("Connecting to R1...")

        connection = ConnectHandler(**router)

        print("Connected to R1 successfully.")

        if router["secret"]:
            connection.enable()

        print("Current prompt:", connection.find_prompt())

        print("\nSending configuration to R1...\n")

        output = connection.send_config_set(
            commands,
            exit_config_mode=True
        )

        print(output)

        print("\nSaving configuration...")

        print(connection.save_config())

        print("\n========================================")
        print("R1 CONFIGURATION COMPLETED SUCCESSFULLY")
        print("========================================")

    except NetmikoTimeoutException:

        print("\nConnection timed out.")

    except NetmikoAuthenticationException:

        print("\nAuthentication failed.")

    except Exception as error:

        print(f"\nUnexpected error: {error}")

    finally:

        if connection is not None:
            connection.disconnect()
            print("\nDisconnected from R1.")


if __name__ == "__main__":
    main()