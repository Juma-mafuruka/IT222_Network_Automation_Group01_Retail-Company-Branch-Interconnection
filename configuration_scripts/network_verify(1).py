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


verification_commands = [
    [
        "R1",
        "show ip interface brief",
        "show ip route",
        "show ip protocols",
        "show run interface Gi0/0",
        "show run interface Gi0/1",
    ],

    [
        "R2",
        "show ip interface brief",
        "show ip route",
        "show ip protocols",
        "show run interface Gi0/0",
        "show run interface Gi0/1",
    ],

    [
        "SW1",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
        "show ip interface brief",
        "show run interface Gi0/1",
        "show run interface Gi0/2",
        "show run interface Gi0/3",
    ],

    [
        "SW2",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
        "show ip interface brief",
        "show run interface Gi0/1",
        "show run interface Gi0/2",
        "show run interface Gi0/3",
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

    for command_group in verification_commands:

        if command_group[0] == device_name:

            commands_for_device = command_group[1:]

            break

    if not commands_for_device:

        print(
            f"\n{device_name}: "
            "No verification commands have been assigned."
        )

        continue

    try:

        print(f"\nConnecting to {device_name}...")

        connection = ConnectHandler(**connection_details)

        print(f"{device_name}: Connected successfully.")

        if connection_details["secret"]:

            connection.enable()

        for command in commands_for_device:

            print(
                f"\n--- {device_name}: {command} ---"
            )

            output = connection.send_command(
                command,
                read_timeout=30
            )

            print(output)

    except NetmikoTimeoutException:

        print(
            f"{device_name}: Connection timed out. "
            "Check the GNS3 VM IP address, TELNET console port, "
            "GNS3 VM, and device state."
        )

    except NetmikoAuthenticationException:

        print(
            f"{device_name}: Authentication failed. "
            "Check the username, password, and enable password."
        )

    except Exception as error:

        print(
            f"{device_name}: Unexpected error: {error}"
        )

    finally:

        if connection is not None:

            connection.disconnect()

            print(
                f"{device_name}: Disconnected."
            )


print("\nNetwork verification completed.")