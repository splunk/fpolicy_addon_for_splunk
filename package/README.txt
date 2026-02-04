FPolicy Add-on for Splunk
Version 1.8.1 (January 14, 2026)

Created and maintained by:
Gurkan Gokdemir (ggokdemir@splunk.com)
Bartosz Debek (bdebek@splunk.com)

===============================================================================
OVERVIEW
===============================================================================

The FPolicy Add-on for Splunk integrates NetApp ONTAP FPolicy Framework with 
Splunk Enterprise, enabling real-time file access monitoring and security 
compliance through File Access Notifications delivered over TCP as XML.

===============================================================================
FEATURES
===============================================================================

- Real-time File Access Monitoring: Capture file operations (create, modify, 
  delete, access) in real-time
- Protocol Support: Monitor CIFS, NFSv3, and NFSv4.x protocols
- SSL/TLS Encryption: Secure data transmission with TLS 1.2 support
- Multi-Node Cluster Support: Connect to up to 8 ONTAP nodes per cluster

===============================================================================
REQUIREMENTS
===============================================================================

- Splunk Enterprise 8.x or later
- ONTAP with FPolicy Framework enabled
- Python 3.7+ (bundled with Splunk)
- TCP connectivity between ONTAP and Splunk

For SSL/TLS:
- Valid SSL certificate and private key (.pem format)
- TLS 1.2 support on ONTAP cluster

===============================================================================
INSTALLATION
===============================================================================

1. Install the add-on in Splunk Enterprise
2. Navigate to the add-on configuration page
3. Create a new data input with the following:
   - Name: Unique identifier for the input
   - Index: Target index for FPolicy events
   - Sourcetype: Custom sourcetype for your data
   - Server IP: Splunk instance IP or 0.0.0.0
   - Server Port: Unused port number (default: 1337)
   - Policy Name: Must match ONTAP FPolicy configuration
   - Use SSL (optional): Enable for TLS 1.2 encryption
     - Upload SA Certificate (.pem file)
     - Upload SA Key (.pem file)

===============================================================================
ONTAP FPOLICY CONFIGURATION
===============================================================================

1. Create FPolicy Event:
   Define events to audit and protocol (CIFS, NFSv3, NFSv4)

2. Create FPolicy External Engine:
   Provide Splunk IP address and TCP port

   Example:
   vserver fpolicy policy external-engine create \
     -vserver <svm_name> \
     -engine-name <engine_name> \
     -primary-servers <splunk_ip> \
     -port <splunk_port> \
     -extern-engine-type asynchronous \
     -ssl-option no-auth \
     -extern-engine-format xml

3. Create FPolicy Policy:
   Link events with external engine

   vserver fpolicy policy create \
     -vserver <svm_name> \
     -policy-name <policy_name> \
     -events <event_name> \
     -engine <engine_name>

4. Create FPolicy Scope:
   Define data to audit (SVM, share, export-policy)

5. Enable FPolicy:
   fpolicy enable -vserver <svm_name> -policy-name <policy_name>

===============================================================================
HANDSHAKE PROCESS
===============================================================================

Negotiation Request:
- Node sends supported FPolicy protocol versions to Splunk
- Waits 2 seconds for response, retries per max-connection-retries

Negotiation Response:
- Splunk responds with selected protocol version
- Node accepts first response, discards duplicates

Negotiation Error:
- If unsupported protocol version sent, node sends error and terminates

XML Schema for Handshake:

The XML Schema fields are described below:

• VsUUID: This field contains the vserver UUID where FPolicy is enabled.

• PolicyName: This field contains the policy name in the vserver for which 
  an external connection is established with the External FPolicy server to 
  provide file notification.

• SessionID: This is a unique identifier created by the storage appliance 
  once a secure connection is established with the External FPolicy server. 
  The External FPolicy server must store the session_id to tag a connection 
  for a policy. The storage appliance will use this session_id in case the 
  connection is broken, and FSM re-establishes the session. The session_id 
  is also useful for VIF movement within the same node.

• ProtVersions: This field contains the protocol version number. In the 
  future, protocol handshake requests might contain multiple protocol 
  versions, as sent by the storage appliance to the External FPolicy server. 
  The External FPolicy server must return one protocol from the list of 
  protocols provided in the Handshake Request.

Example Handshake Messages:

Negotiation Request:
<?xml version="1.0"?>
<Header>
  <NotfType>NEGO_REQ</NotfType>
  <ContentLen>287</ContentLen>
  <DataFormat>XML</DataFormat>
</Header>
<?xml version="1.0"?>
<Handshake>
  <VsUUID>45228b37-6292-11ee-b5d1-000c29cdbe04</VsUUID>
  <PolicyName>policy-test</PolicyName>
  <SessionId>d8ad84cc-79dd-11ee-b638-000c29cdbe04</SessionId>
  <ProtVersion>
    <Vers>1.0</Vers>
    <Vers>1.1</Vers>
    <Vers>1.2</Vers>
    <Vers>2.0</Vers>
  </ProtVersion>
</Handshake>

Negotiation Response:
<?xml version="1.0"?>
<Header>
  <NotfType>NEGO_RESP</NotfType>
  <ContentLen>234</ContentLen>
  <DataFormat>XML</DataFormat>
</Header>
<?xml version="1.0"?>
<HandshakeResp>
  <VsUUID>45228b37-6292-11ee-b5d1-000c29cdbe04</VsUUID>
  <PolicyName>policy-test</PolicyName>
  <SessionId>d8ad84cc-79dd-11ee-b638-000c29cdbe04</SessionId>
  <ProtVersion>1.2</ProtVersion>
</HandshakeResp>

Keep Alive Messages:
<?xml version="1.0"?>
<Header>
  <NotfType>KEEP_ALIVE</NotfType>
  <ContentLen>0</ContentLen>
  <DataFormat>XML</DataFormat>
</Header>

===============================================================================
IMPORTANT CONFIGURATION NOTES
===============================================================================

- Policy name in add-on MUST match ONTAP FPolicy configuration
- Server IP can be specific IP or 0.0.0.0 for all interfaces
- Each input requires a unique port number
- Certificates stored in: $SPLUNK_HOME/etc/apps/fpolicy_addon_for_splunk/certs/

===============================================================================
SUPPORT
===============================================================================

⚠️ IMPORTANT: This add-on is not officially supported by Splunk.

Do not open support tickets with Splunk Support.

For issues and feature requests:
GitHub Issues: https://github.com/splunk/fpolicy_addon_for_splunk/issues

If using this add-on, please mention it to your Splunk account team 
(Regional Sales Manager and Solutions Engineer) to help support the case 
for official Splunk support.

===============================================================================
TROUBLESHOOTING
===============================================================================

Network Connection Tests:

Use these commands to verify connectivity between Splunk and ONTAP:

1. Check if port is open:
   nmap -p <port> <ontap_ip>

2. Verify port is listening:
   netstat -ant | grep <port>

3. Monitor incoming traffic:
   tcpdump dst port <port>
   tcpdump src <ontap_ip>

4. Check public IP (if needed):
   curl ifconfig.me

Common Issues:

- Handshake fails: Verify policy name matches exactly in both ONTAP and add-on
- No data received: Check firewall rules and TCP connectivity
- SSL errors: Verify certificate format (.pem) and TLS 1.2 compatibility

===============================================================================
RESOURCES
===============================================================================

- GitHub Repository: https://github.com/splunk/fpolicy_addon_for_splunk
- .conf24 Presentation (THE2817): Enhancing Visibility with Splunk and NetApp FPolicy
  https://docs.google.com/presentation/d/1uKmHYD2VlyRCGZHJVN4KFEXbR1GZQg93g2Su9LhJjDI

===============================================================================
SECURITY CONSIDERATIONS
===============================================================================

SSL/TLS for FPolicy Connections:
The add-on supports TLS 1.2 encryption for connections between NetApp ONTAP 
and the Splunk add-on server. When SSL is enabled, the connection uses 
customer-provided certificates for secure communication.

Splunk SDK SSL Verification:
The bundled Splunk SDK (splunk-sdk) uses verify=False as the default for SSL 
connections to the Splunk REST API. This is a known behavior in the upstream 
Splunk SDK to support backward compatibility with various deployment 
configurations.

Risk Assessment: Low - The SDK connects to the local Splunk instance's REST 
API (typically localhost:8089), limiting exposure to man-in-the-middle 
attacks. The connection remains encrypted; only certificate verification 
is disabled.

===============================================================================
LICENSE
===============================================================================

Apache License 2.0 - See LICENSE.txt for details

===============================================================================
VERSION HISTORY
===============================================================================

1.8.1 (2026-01-14) - SSL/TLS encryption support, removed deprecated Accounts
1.7.6 (2024-05-09) - Sourcetype selection, support for up to 8 nodes per cluster
1.5.6 (2024-04-11) - Full cluster support
1.3.3 (2024-03-28) - Single SVM node support
0.7.1 (2023-12-20) - Logging updates
0.6.5 (2023-10-20) - Initial release
