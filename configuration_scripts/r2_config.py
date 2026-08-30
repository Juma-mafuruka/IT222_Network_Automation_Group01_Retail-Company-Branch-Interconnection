from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start R1 in GNS3 before running this script.
# Enter the connection details for R1.
# Use the current GNS3 VM/server IP address and R1 TELNET console port.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.31.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5002,
}


# Enter the Cisco IOS commands required to configure R1
# according to the current network topology.
commands = [
    "hostname R2",

 "interface gigabitEthernet0/0",
    "description TRUNK_TO_SW2",
    "no shutdown",
    "exit",

    "interface gigabitEthernet0/0.10",
    "description SALES_VLAN_10",
    "encapsulation dot1Q 10",
    "ip address 192.168.30.1 255.255.255.0",
    "no shutdown",
    "exit",

    "interface gigabitEthernet0/0.20",
    "description MANAGER_VLAN_20",
    "encapsulation dot1Q 20",
    "ip address 192.168.40.1 255.255.255.0",
    "no shutdown",
    "exit",

    "interface gigabitEthernet0/1",
    "description LINK_TO_R1",
    "ip address 10.1.1.2 255.255.255.252",
    "no shutdown",
    "exit",

    "ip route 192.168.10.0 255.255.255.0 10.1.1.1",
    "ip route 192.168.20.0 255.255.255.0 10.1.1.1",
    
]


connection = None

try:
    # Connect to R1 through the GNS3 TELNET console.
    connection = ConnectHandler(**router)

    # Enter privileged EXEC mode if an enable password is configured.
    if router["secret"]:
        connection.enable()

    # Send the configuration commands to R1.
    output = connection.send_config_set(commands)
    print(output)

    # Save the configuration.
    connection.save_config()

    print("\nR1 configuration completed successfully.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "R1 TELNET console port, GNS3 VM, and router state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session if a connection was opened.
    if connection is not None:
        connection.disconnect()