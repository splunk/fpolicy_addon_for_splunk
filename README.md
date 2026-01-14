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
- [Author](#author)

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
   - **Name**: Provide a unique name for the configuration.
   - **Index**: Select or create an appropriate index for storing FPolicy events.
   - **Account**: Use an account with necessary permissions.
   - **IP**: Enter the local instance IP or `0.0.0.0`.
   - **Port**: Specify any unused port.
   - **Policy Name**: Ensure it matches the FPolicy configuration for a successful handshake.

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

## Authors

Gurkan Gokdemir (ggokdemir@splunk.com)
Bartosz Debek (bdebek@splunk.com)
