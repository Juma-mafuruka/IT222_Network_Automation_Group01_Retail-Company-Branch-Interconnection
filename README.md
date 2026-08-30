# Network Automation - IT222 Group01

## Assignment Identification
**Course: IT 222**
**Assignment Number: 01**

**Scenario:** A retail company operates two outlets. Sales terminals process customer purchases, while
management computers support stock supervision and administrative activities. The outlets must be interconnected while Sales and Management traffic remain logically
separated.

**Group Number:1**

## Group members
- **JUMA LUSHUGEMBE MAFURUKA RegNo 2024/1800**
- **HAMPHREY FRANK SONNA    RegNo 2024/0125**
- **AYUBU ROBERT MMALI  RegNo 2024/1015**
- **EFSIBA STEVEN ANDULILE RegNo 2024/1787**

## Scenario Description
This folder contains Python scripts for configuring, verifying, and testing a multi-device network topology using Netmiko.

## Network Topology Overview

The configured network consists of:

- **2 Routers**: R1 and R2 connected via a point-to-point link
- **2 Switches**: SW1 (connected to R1) and SW2 (connected to R2)
- **2 VLANs**: VLAN 10 (Sales) and VLAN 20 (Management)

### Network Layout

```
┌─────────────────────────────────────────────────────────────┐
│                   Inter-Router Link (10.1.1.0/30)           │
│         R1 (10.1.1.1) ════════════════ R2 (10.1.1.2)        │
│              ║                              ║               │
│          GE0/0 (Trunk)                  GE0/0 (Trunk)       │
│              ║                              ║               │
│           ┌──┴──┐                        ┌──┴──┐            │
│           │ SW1 │                        │ SW2 │            │
│           └─┬─┬─┘                        └─┬─┬─┘            │
│             │ │                            │ │              │
│         GE0/2│ │GE0/3                 GE0/2│ │GE0/3         │
│             │ │                            │ │              │
│      ┌──────┘ └──────┐            ┌──────┘ └──────┐        │
│      │               │            │               │         │
│   Sales PC1    Manager PC1     Sales PC2    Manager PC2    │
│  (VLAN 10)      (VLAN 20)      (VLAN 10)     (VLAN 20)     │
│ 192.168.10.x   192.168.20.x   192.168.30.x  192.168.40.x  │
└─────────────────────────────────────────────────────────────┘
```

### IP Address Summary

| Device  | VLAN 10 (Sales)  | VLAN 20 (Management) | Link IP          |
|---------|------------------|----------------------|------------------|
| R1      | 192.168.10.1/24  | 192.168.20.1/24      | 10.1.1.1/30      |
| SW1     | 192.168.10.2/24  | 192.168.20.2/24      | -                |
| R2      | 192.168.30.1/24  | 192.168.40.1/24      | 10.1.1.2/30      |
| SW2     | 192.168.30.2/24  | 192.168.40.2/24      | -                |

## 1. Device Configuration Scripts

### Router Configurations

**Router R1** (`r1_config.py`):
- Hostname: R1
- VLAN 10 Subinterface: 192.168.10.1/24 (Sales)
- VLAN 20 Subinterface: 192.168.20.1/24 (Management)
- Uplink to R2: 10.1.1.1/30
- Trunk interface to SW1: GigabitEthernet0/0
- Static routes to R2's networks

**Router R2** (`r2_config.py`):
- Hostname: R2
- VLAN 10 Subinterface: 192.168.30.1/24 (Sales)
- VLAN 20 Subinterface: 192.168.40.1/24 (Management)
- Uplink to R1: 10.1.1.2/30
- Trunk interface to SW2: GigabitEthernet0/0
- Static routes to R1's networks

### Switch Configurations

**Switch SW1** (`sw1_config.py`):
- Hostname: SW1
- VLAN 10: Sales (SVI IP: 192.168.10.2/24)
- VLAN 20: Management (SVI IP: 192.168.20.2/24)
- GE0/1: Trunk to R1
- GE0/2: Access port (VLAN 10) - Sales PC
- GE0/3: Access port (VLAN 20) - Management PC
- Default Gateway: 192.168.20.1 (R1 VLAN 20)

**Switch SW2** (`sw2_config.py`):
- Hostname: SW2
- VLAN 10: Sales (SVI IP: 192.168.30.2/24)
- VLAN 20: Management (SVI IP: 192.168.40.2/24)
- GE0/1: Trunk to R2
- GE0/2: Access port (VLAN 10) - Sales PC
- GE0/3: Access port (VLAN 20) - Management PC
- Default Gateway: 192.168.40.1 (R2 VLAN 20)

## 2. Device Verification and Testing Scripts

Each device has two additional scripts:

- `*_verify.py`: Verifies device configuration (running config, interface status, IP addresses)
- `*_test.py`: Tests device connectivity and functionality

**Available device scripts:**
```
r1_config.py, r1_verify.py, r1_test.py
r2_config.py, r2_verify.py, r2_test.py
sw1_config.py, sw1_verify.py, sw1_test.py
sw2_config.py, sw2_verify.py, sw2_test.py
```

## 3. Network-Level Scripts

**Network Verification** (`network_verify.py`):
- Collects information from all devices (R1, R2, SW1, SW2)
- Verifies VLAN configuration across switches
- Confirms routing connectivity between routers
- Checks IP address assignments on all interfaces

**Network Testing** (`network_test.py`):
- Performs end-to-end connectivity tests between VLANs
- Tests inter-router communication via the 10.1.1.0/30 link
- Verifies cross-network connectivity (e.g., Sales on SW1 to Sales on SW2)
- Validates management VLAN connectivity across both sites

## 4. Recommended Workflow

Execute the scripts in the following sequence to ensure proper network setup:

```
1. Configure Individual Devices
   ├── python r1_config.py       (Configure Router R1)
   ├── python r2_config.py       (Configure Router R2)
   ├── python sw1_config.py      (Configure Switch SW1)
   └── python sw2_config.py      (Configure Switch SW2)

2. Verify Individual Devices
   ├── python r1_verify.py       (Verify R1 configuration)
   ├── python r2_verify.py       (Verify R2 configuration)
   ├── python sw1_verify.py      (Verify SW1 configuration)
   └── python sw2_verify.py      (Verify SW2 configuration)

3. Test Individual Devices
   ├── python r1_test.py         (Test R1 connectivity)
   ├── python r2_test.py         (Test R2 connectivity)
   ├── python sw1_test.py        (Test SW1 operations)
   └── python sw2_test.py        (Test SW2 operations)

4. Verify Integrated Network
   └── python network_verify.py  (Verify multi-device configuration)

5. Test End-to-End Connectivity
   └── python network_test.py    (Test complete network operation)
```

**Rationale**: This sequence isolates problems at the device level before troubleshooting the integrated network.

## 5. GNS3 Connection Details

All devices connect to the GNS3 VM at `192.168.31.128` using TELNET:

| Device | Port | Type   |
|--------|------|--------|
| R1     | 5000 | Router |
| R2     | 5002 | Router |
| SW1    | 5004 | Switch |
| SW2    | 5006 | Switch |

**Note**: Update connection details in each script if your GNS3 VM IP address or TELNET ports differ.

## 6. File Structure

```
IT222_Network_Automation_Group01/
│
├── README.md                          (This file)
├── requirements.txt                   (Python dependencies)
│
├── Configuration Scripts
│   ├── r1_config.py                  (R1 configuration)
│   ├── r2_config.py                  (R2 configuration)
│   ├── sw1_config.py                 (SW1 configuration)
│   └── sw2_config.py                 (SW2 configuration)
│
├── Verification Scripts
│   ├── r1_verify.py                  (Verify R1)
│   ├── r2_verify.py                  (Verify R2)
│   ├── sw1_verify.py                 (Verify SW1)
│   ├── sw2_verify.py                 (Verify SW2)
│   └── network_verify.py              (Verify entire network)
│
├── Testing Scripts
│   ├── r1_test.py                    (Test R1)
│   ├── r2_test.py                    (Test R2)
│   ├── sw1_test.py                   (Test SW1)
│   ├── sw2_test.py                   (Test SW2)
│   └── network_test.py                (Test entire network)
│
└── Templates (Reference)
    ├── router_config_template.py      (Router configuration template)
    ├── router_verify_template.py      (Router verification template)
    ├── router_test_template.py        (Router testing template)
    ├── switch_config_template.py      (Switch configuration template)
    ├── switch_verify_template.py      (Switch verification template)
    ├── switch_test_template.py        (Switch testing template)
    ├── network_verify_template.py     (Network verification template)
    └── network_test_template.py       (Network testing template)
```

## 7. Extending the Network

To add additional devices to this topology:

### Adding More Routers

1. Copy `router_config_template.py` and rename to `r3_config.py`
2. Update connection details (IP, port, credentials)
3. Modify configuration commands for the new topology
4. Create `r3_verify.py` and `r3_test.py` following the same pattern

### Adding More Switches

1. Copy `switch_config_template.py` and rename to `sw3_config.py`
2. Update connection details
3. Modify VLAN and interface configurations
4. Create `sw3_verify.py` and `sw3_test.py` following the same pattern

### Adding Other Device Types

Docker containers, firewalls, or other devices can follow similar naming conventions:

```
server1_verify.py, server1_test.py
firewall1_config.py, firewall1_verify.py, firewall1_test.py
```

## 8. Requirements

- Python 3.7+
- Netmiko library (for Cisco device automation)
- GNS3 with Cisco IOS images and network topology running
- Network connectivity between your host and GNS3 VM

Install dependencies:

```bash
pip install -r requirements.txt
```

## 9. Security Notes

- Credentials (username/password) in the scripts are currently empty placeholders
- Update with actual GNS3 lab credentials before running
- Never commit credentials to version control
- Use environment variables or external config files for sensitive data in production

## 10. Troubleshooting

### Connection Issues
- Verify GNS3 VM is running and reachable at 192.168.31.128
- Check that TELNET ports (5000, 5002, 5004, 5006) are accessible
- Confirm device is booted and ready for configuration
- Review credentials in the connection dictionary

### Configuration Issues
- Verify the running IOS version supports the commands used
- Check interface names and port numbers match your topology
- Ensure VLAN numbering is consistent across all devices
- Review error messages from Netmiko for device-specific issues

### Network Connectivity Issues
- Verify routing configuration with `show ip route` commands in verification scripts
- Check VLAN membership on trunk interfaces
- Confirm static routes are correctly configured
- Use network_verify.py to check multi-device configuration consistency
