# FPolicy Add-on for Splunk

NetApp ONTAP FPolicy Add-on for Splunk allows Splunk admins to get File Access Notifications over network port (TCP) as XML Notifications into the Splunk platform for the NetApp ONTAP FPolicy Framework that manages NetApp SVMs.

## Table of Contents

- [Requirements](#requirements)
- [Add-on Information](#add-on-information)
- [Setup and Configuration](#setup-and-configuration)
  - [FPolicy Add-on for Splunk Setup](#fpolicy-add-on-for-splunk-setup)
  - [ONTAP FPolicy Setup](#ontap-fpolicy-setup)
  - [FPolicy Policy Configuration](#fpolicy-policy-configuration)
  - [Handshake Process](#handshake-process)
  - [Troubleshooting](#troubleshooting)
  - [Network Connection Tests](#network-connection-tests)
- [File Access Auditing](#file-access-auditing)
- [FPolicy Framework](#fpolicy-framework)
- [FPolicy Add-on for Splunk](#fpolicy-add-on-for-splunk)
- [Overall Topology and Handshake Process](#overall-topology-and-handshake-process)
- [Authentication Mechanisms](#authentication-mechanisms)
- [Integrated Monitoring and Alerting](#integrated-monitoring-and-alerting)
- [Development and Building](#development-and-building)
  - [Prerequisites for Development](#prerequisites-for-development)
  - [Building the Add-on](#building-the-add-on)
  - [Development Reference](#development-reference)
- [Authors](#authors)

## Requirements

- ONTAP FPolicy Framework ready for policy configuration.
- Splunk Enterprise to install the FPolicy Add-on (as an external server).
- Network connection between the end user, ONTAP FPolicy, and Splunk Enterprise.

## Add-on Information

- **Version 0.6.5 (20/10/2023):** Initial tests with cloud instance completed.
- **Version 0.7.1 (20/12/2023):** Logging updates (`splunk/var/log/splunk/server_input.log`).
- **Version 1.3.3 (28/03/2024):** Single SVM node support.
- **Version 1.5.6 (11/04/2024):** Full cluster support.
- **Version 1.7.6 (09/05/2024):** Sourcetype selection, support for up to 8 nodes per cluster, resolved intermittent issues.
- **Version 1.8.1 (14/01/2026):** SSL/TLS encryption support, removed deprecated Accounts section.

### Notes

- Set the external server IP as the device IP (or leave it as `0.0.0.0`); the port number should be any unused port number.
- Match the policy name in ONTAP FPolicy for a proper handshake.

## Setup and Configuration

### FPolicy Add-on for Splunk Setup

1. **Download and Install the Add-on**:
   - Obtain the FPolicy Add-on from Splunkbase or your internal repository.
   - Install the Add-on in Splunk Enterprise.

2. **Configuration**:
   - **Name**: Provide a unique name for the data input.
   - **Index**: Select or create an appropriate index for storing FPolicy events.
   - **Sourcetype**: Define a unique sourcetype for the data.
   - **Add-on Server IP**: Enter the external IP of the Splunk instance or `0.0.0.0` (default: `0.0.0.0`).
   - **Add-on Server Port**: Specify any unused port number for each input (default: `1337`).
   - **Policy Name**: FPolicy File Policy Name - must match the FPolicy configuration for a successful handshake.
   - **Use SSL** (optional): Enable SSL/TLS encryption for ONTAP connection.
     - **SA Certificate**: Upload server-side SSL certificate (.pem or .txt file).
     - **SA Key**: Upload server-side SSL key (.pem or .txt file).

### ONTAP FPolicy Setup

Follow the NetApp ONTAP FPolicy guidelines for detailed instructions.

### FPolicy Policy Configuration

1. **Create FPolicy Event**: Define the events to audit (e.g., create, delete, write) and the protocol (CIFS, NFSv3, NFSv4).
2. **Create FPolicy External Engine**: Provide the IP address and TCP port of the add-on.
3. **Create FPolicy Policy**: Link events with the external engine.
4. **Create FPolicy Scope**: Define the data to audit (e.g., SVM, share, export-policy).
5. **Enable FPolicy**: Activate the policy.

### Handshake Process

#### Negotiation Request

- The node sends supported FPolicy protocol versions to the external server (Splunk).
- Waits for two seconds for a response, and retries as per `max-connection-retries`.

#### Negotiation Response

- The external server (Splunk) responds with the selected protocol version.
- The node accepts the first response and discards duplicates.

#### Negotiation Error

- If an unsupported protocol version is sent, the node sends an error, alerts the external server, and terminates the connection.

### Troubleshooting

1. Verify the external server (Splunk) response.
2. Ensure the ONTAP FPolicy node sends a negotiation request.
3. Monitor network traffic using tools like Wireshark.
4. Confirm successful configuration and handshake on ONTAP FPolicy.
5. Ensure the external server (Splunk) receives XML notifications.

### Network Connection Tests

Use Wireshark to monitor traffic and run the following commands:

```bash
nc <client_ip> <client_port> < response.xml
curl ifconfig.me
nmap -p <port> <ip>
netstat -ant | grep <port>
tcpdump dst port <port>
tcpdump src <ip>
```

## File Access Auditing

File Access Auditing (FAA) involves monitoring file access via CIFS, NFSv3, or NFSv4.x protocols on NTFS and Unix file systems. It records actions such as creation, modification, deletion, and access of files.

## FPolicy Framework

FPolicy is an ONTAP component for real-time monitoring and setting file access permissions, crucial for security and compliance.

## FPolicy Add-on for Splunk

The add-on enhances Splunk's capabilities by integrating file event notifications from NetApp, allowing real-time monitoring and analysis of file operations for security and compliance.

## Overall Topology and Handshake Process

A TCP/IP connection is established between each node and the FPolicy Add-on for Splunk. The handshake process ensures secure communication, with the add-on supporting ASYNC Mode and TCP layer acknowledgment.

## Authentication Mechanisms

The handshake is initiated by the policy, requiring admin rights. The policy name in the add-on configuration must match the FPolicy configuration. TCP ensures secure and reliable data transmission, with SSL support for secure data transmission.

## Integrated Monitoring and Alerting

Using `props.conf` and `transforms.conf`, Splunk extracts fields from raw data logs, filters unnecessary parts, and anonymizes certain information. The integration supports automated alerts based on FPolicy events, enhancing security and compliance.

## Development and Building

### Prerequisites for Development

- Python 3.7+
- Splunk UCC Generator (`pip install splunk-add-on-ucc-framework`)
- Access to the fpolicy_addon_for_splunk source repository

### Building the Add-on

If you want to contribute to the add-on or build it from source:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/splunk/fpolicy_addon_for_splunk.git
   cd fpolicy_addon_for_splunk/fpolicy_addon_for_splunk
   ```

2. **Build the add-on**:

   ```bash
   ucc-gen build --ta-version 1.8.1
   ```

3. **Package the add-on**:

   ```bash
   ucc-gen package --path output/fpolicy_addon_for_splunk
   ```

The packaged archive will be created in the same directory as your `globalConfig.json` file.

### Development Reference

For detailed UCC framework documentation and development guidelines, see:

- [UCC Generator Quickstart](https://splunk.github.io/addonfactory-ucc-generator/quickstart/)
- [Splunk Add-on UCC Framework Documentation](https://splunk.github.io/addonfactory-ucc-generator/)

## Authors

Gurkan Gokdemir (ggokdemir@splunk.com)
Bartosz Debek (bdebek@splunk.com)
