# FPolicy Add-on for Splunk

![Version](https://img.shields.io/badge/version-1.8.1-blue)
![Splunk](https://img.shields.io/badge/Splunk-Enterprise-green)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Support](https://img.shields.io/badge/support-community-orange)

NetApp ONTAP FPolicy Add-on for Splunk allows Splunk admins to get File Access Notifications over network port (TCP) as XML Notifications into the Splunk platform for the NetApp ONTAP FPolicy Framework that manages NetApp SVMs.

---

## Features

- **Real-time File Access Monitoring**: Capture file operations (create, modify, delete, access) in real-time
- **Protocol Support**: Monitor CIFS, NFSv3, and NFSv4.x protocols
- **SSL/TLS Encryption**: Secure data transmission with TLS 1.2 support (v1.8.1+)
- **Multi-Node Cluster Support**: Connect to up to 8 ONTAP nodes per cluster

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Version History](#version-history)
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
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Resources](#resources)
- [Authors](#authors)

---

## Requirements

| Component | Requirement |
|-----------|-------------|
| Splunk Enterprise | 8.x or later |
| ONTAP | FPolicy Framework enabled |
| Python | 3.7+ (bundled with Splunk) |
| Network | TCP connectivity between ONTAP and Splunk |

**Additional requirements for SSL/TLS:**
- Valid SSL certificate and private key (.pem format)
- TLS 1.2 support on ONTAP cluster

## Version History

**Current Version**: 1.8.1 (January 14, 2026)

For detailed version history and release notes, see [CHANGELOG.md](CHANGELOG.md).

### Important Configuration Notes

- Set the external server IP as the device IP (or leave it as `0.0.0.0`); the port number should be any unused port number.
- Match the policy name in ONTAP FPolicy for a proper handshake.

---

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
   - **Use SSL** (optional): Enable TLS 1.2 encryption for ONTAP connection.
     - **SA Certificate**: Upload server-side SSL certificate (.pem or .txt file, max 100KB). Required when SSL is enabled.
     - **SA Key**: Upload server-side SSL private key (.pem or .txt file, max 100KB). Required when SSL is enabled.
     - **Note**: Certificates are stored in `$SPLUNK_HOME/etc/apps/fpolicy_addon_for_splunk/certs/` directory.

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

---

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

---

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

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.txt](package/LICENSE.txt) file for details.

---

## Support

> **⚠️ IMPORTANT**: **This add-on is not officially supported by Splunk.** Please do not open support tickets with Splunk Support. Use the GitHub Issues page below for all support requests.

If you're using this add-on in your environment, please consider mentioning it to your Splunk account team (Regional Sales Manager and Solutions Engineer). User adoption and feedback help demonstrate the value of this integration and support the case for official Splunk support.

For issues and feature requests, please use the [GitHub Issues](https://github.com/splunk/fpolicy_addon_for_splunk/issues) page.

For general questions about Splunk, visit [Splunk Answers](https://community.splunk.com/).

---

## Resources

- [**.conf24 Builder Bar Theater Session (THE2817)**: Enhancing Visibility with Splunk and NetApp FPolicy](https://docs.google.com/presentation/d/1uKmHYD2VlyRCGZHJVN4KFEXbR1GZQg93g2Su9LhJjDI) - Presentation from the .conf24 Builder Bar Theater
- [**Implementing File Access Auditing with NetApp FPolicy**](docs/implementing-file-access-auditing-with-netapp-fpolicy.pdf) - Splunk Lantern article covering implementation details

## Authors

Created and maintained by:

- **Gurkan Gokdemir** - [ggokdemir@splunk.com](mailto:ggokdemir@splunk.com)
- **Bartosz Debek** - [bdebek@splunk.com](mailto:bdebek@splunk.com)

---

**Questions or feedback?** Open an issue on [GitHub](https://github.com/splunk/fpolicy_addon_for_splunk/issues) or contact the authors directly.
