from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

devices = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.31.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5000,
    },
    {
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.31.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5002,
    },
    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.31.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5004,
    },
    {
        "name": "SW2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.31.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5006,
    },
]

testing_commands = [
    [
        "R1",
        "ping 10.1.1.1", # R1 gateway
        "ping 10.1.1.2", # R2 gateway
        "ping 192.168.30.10", # sales2 IP
        "traceroute 192.168.30.10", # sales2 traceroute
        "ping 192.168.30.1", # sales2 gateway
        "ping 192.168.40.1", # management2 gateway
        "ping 192.168.40.10", # management2 IP
        "traceroute 192.168.40.10", # management2 traceroute
        "ping 192.168.10.10", # sales1 IP
        "traceroute 192.168.10.10", # sales1 traceroute
        "ping 192.168.20.10", # management1 IP
        "traceroute 192.168.20.10", # management1 traceroute
    ],
    [
        "R2",
        "ping 10.1.1.1", # R1 gateway
        "ping 10.1.1.2", # R2 gateway
        "ping 192.168.30.10", # sales2 IP
        "traceroute 192.168.30.10", # sales2 traceroute
        "ping 192.168.30.1", # sales2 gateway
        "ping 192.168.40.1", # management2 gateway
        "ping 192.168.40.10", # management2 IP
        "traceroute 192.168.40.10", # management2 traceroute
        "ping 192.168.10.10", # sales1 IP
        "traceroute 192.168.10.10", # sales1 traceroute
        "ping 192.168.20.10", # management1 IP
        "traceroute 192.168.20.10", # management1 traceroute
    ],
    [
        "SW1",
         "ping 192.168.10.1", # sales1 gateway
         "ping 192.168.20.1", # management1 gateway
         "ping  192.168.10.10", # sales1 IP
         "ping 192.168.20.10" # management1 IP
       
    ],
    [
        "SW2",
       
        "ping 192.168.40.1", # management2 gateway
        "ping 192.168.30.1", # sales2 gateway
        "ping 192.168.30.10", # sales2 IP
        "ping 192.168.40.10" # management2 IP
    ],
]

for device in devices:

    connection = None
    device_name = device["name"]

    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }

    commands_for_device = []

    for command_group in testing_commands:
        if command_group[0] == device_name:
            commands_for_device = command_group[1:]
            break

    if not commands_for_device:
        print(f"\n{device_name}: No network tests have been assigned.")
        continue

    try:

        print(f"\nConnecting to {device_name}...")

        connection = ConnectHandler(**connection_details)

        print(f"{device_name}: Connected successfully.")

        if connection_details["secret"]:
            connection.enable()

        for command in commands_for_device:

            print(f"\n--- {device_name}: Testing {command} ---")

            output = connection.send_command(
                command,
                read_timeout=30,
            )

            print(output)

    except NetmikoTimeoutException:

        print(
            f"{device_name}: Connection timed out. "
            "Check GNS3 VM IP, TELNET port, GNS3 VM, "
            "and device state."
        )

    except NetmikoAuthenticationException:

        print(
            f"{device_name}: Authentication failed. "
            "Check username, password, and enable password."
        )

    except Exception as error:

        print(f"{device_name}: Unexpected error: {error}")

    finally:

        if connection is not None:
            connection.disconnect()

            print(f"{device_name}: Disconnected.")

print("\nNetwork testing completed.")