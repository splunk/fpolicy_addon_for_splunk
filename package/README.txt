FPolicy Add-on for Splunk
========================
Version 1.8.1

NetApp ONTAP FPolicy Add-on for Splunk allows Splunk admins to get File Access
Notifications over network port (TCP) as XML Notifications into the Splunk
platform for the NetApp ONTAP FPolicy Framework that manages NetApp SVMs.


REQUIREMENTS
------------
- Splunk Enterprise 8.x or later
- ONTAP FPolicy Framework enabled
- Python 3.7+ (bundled with Splunk)
- TCP connectivity between ONTAP and Splunk

Additional requirements for SSL/TLS:
- Valid SSL certificate and private key (.pem format)
- TLS 1.2 support on ONTAP cluster


SETUP AND CONFIGURATION
-----------------------

FPolicy Add-on for Splunk Setup:

1. Download and Install the Add-on:
   - Obtain the FPolicy Add-on from Splunkbase or your internal repository.
   - Install the Add-on in Splunk Enterprise.

2. Configuration Fields:
   - Name: Provide a unique name for the data input.
   - Index: Select or create an appropriate index for storing FPolicy events.
   - Sourcetype: Define a unique sourcetype for the data.
   - Add-on Server IP: Enter the external IP of the Splunk instance or 0.0.0.0
   - Add-on Server Port: Specify any unused port number (default: 1337)
   - Policy Name: FPolicy File Policy Name - must match ONTAP FPolicy config
   - Use SSL (optional): Enable TLS 1.2 encryption for ONTAP connection
     - SA Certificate: Upload server-side SSL certificate (.pem, max 100KB)
     - SA Key: Upload server-side SSL private key (.pem, max 100KB)

   Note: Certificates are stored in:
   $SPLUNK_HOME/etc/apps/fpolicy_addon_for_splunk/certs/


ONTAP FPOLICY SETUP
-------------------

1. Create FPolicy External Engine:
   vserver fpolicy policy external-engine create -vserver <svm> \
     -engine-name <engine> -primary-servers <splunk_ip> -port <port> \
     -extern-engine-type asynchronous -ssl-option no-auth \
     -extern-engine-format xml

   For SSL-enabled connections, use: -ssl-option server-auth

2. Create FPolicy Event:
   vserver fpolicy policy event create -vserver <svm> \
     -event-name <event> -volume-operation false -protocol cifs \
     -file-operations open,read,write,rename,create

3. Create FPolicy Policy:
   vserver fpolicy policy create -vserver <svm> -policy-name <policy> \
     -events <event> -engine <engine> -is-mandatory false

4. Create FPolicy Scope:
   fpolicy policy scope create -vserver <svm> -policy-name <policy> \
     -volumes-to-include <volume>

5. Enable FPolicy:
   fpolicy enable -vserver <svm> -policy-name <policy> -sequence-number 1


HANDSHAKE PROCESS
-----------------

Negotiation Request:
- The ONTAP node sends supported FPolicy protocol versions to Splunk.
- Waits 2 seconds for response, retries per max-connection-retries setting.

Negotiation Response:
- Splunk responds with selected protocol version (1.2).
- Node accepts first response, discards duplicates.

Negotiation Error:
- If unsupported protocol version sent, node generates error and terminates.


TROUBLESHOOTING
---------------

1. Verify the external server (Splunk) response.
2. Ensure the ONTAP FPolicy node sends a negotiation request.
3. Monitor network traffic using tools like Wireshark.
4. Confirm successful configuration and handshake on ONTAP FPolicy.
5. Ensure the external server (Splunk) receives XML notifications.

Network Connection Tests:
   nc <client_ip> <client_port> < response.xml
   nmap -p <port> <ip>
   netstat -ant | grep <port>
   tcpdump dst port <port>

FPolicy Status Commands:
   fpolicy show
   fpolicy show-engine
   fpolicy policy show -instance


LICENSE
-------
Apache License 2.0 - See LICENSE.txt for details.


SUPPORT
-------
For issues and feature requests:
https://github.com/splunk/fpolicy_addon_for_splunk/issues


AUTHORS
-------
Gurkan Gokdemir (ggokdemir@splunk.com)
Bartosz Debek (bdebek@splunk.com)
