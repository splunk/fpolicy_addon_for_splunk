FPolicy Add-on for Splunk | Add-on Test and Development Setup (Confidential)
Gurkan Gokdemir (ggokdemir@splunk.com)
Goal
Overall: Create a test environment to test FPolicy Add-on for Splunk integration.
Required
ONTAP FPolicy Framework ready for Policy configuration.
Splunk Enterprise to install FPolicy Add-on for Splunk (As an External Server)
End User (User that manipulates SVM for event creation.)
Network Connection between End User, ONTAP FPolicy, and Splunk Enterprise.
More Info About the Add-on
The FPolicy Add-on for Splunk:
(20/10/2023) version 0.6.5 → Initial tests with cloud instance done.
(20/12/2023) version 0.7.1 → Logging update. (splunk/var/log/splunk/server_input.log)

Under the same subnet, it should be able to send and process;
KEEP_ALIVE.xml, NEGO_REQ.xml, and SCREEN_REQ.xml

The add-on can process them as expected.

Notes:
External Server IP needs to be set as the device IP. Only the Port number is optional.
The policy Name should be the same as in the ONTAP FPolicy to have a proper handshake.

More Info About the Handshake Process
Negotiation Request (Handshake Request)
After establishing a secure connection between the External FPolicy server (Splunk) and the node, the node sends the FPolicy protocol versions that it supports to the External FPolicy server (Splunk).
After sending the Negotiation Request, the node waits for two seconds for the External FPolicy server (Splunk) to respond. If a response is not received within two seconds, the node resends the Negotiation Request.
This process repeats as many times as specified in the max-connection-retries input attribute. If a response is not received, the node stops sending Negotiation Requests to the External FPolicy server (Splunk).
Negotiation Response (Handshake Response)
Once the node sends the list of FPolicy protocol versions that it supports via the Negotiation Request, the External FPolicy server (Splunk) must respond with a Negotiation Response that specifies the protocol version it would like to use to communicate with the node.
The node accepts the first response it receives and will discard any duplicate or later responses that it receives from other External FPolicy server (Splunk).
Negotiation Error
When the External FPolicy server (Splunk) sends a Negotiation Response with a protocol version the node does not support, the node generates an error message.
In that scenario, the node sends an alert message to the External FPolicy server (Splunk) and terminates the connection. The alert message contains the reason for the disconnection.
To-do
Send XML format data over TCP (Examples are below) to the External FPolicy server (Splunk) to see the response. (To confirm the Add-on will work as expected.)
Then set the ONTAP FPolicy node to send a Negotiation Request. (Monitor the traffic if possible via Wireshark.)
Confirm if the configuration and handshake are successful on the ONTAP FPolicy side.
 Confirm if the External FPolicy server (Splunk) receives the XML notifications.

XML Schema for Handshake Response.
The XML Schema fields are described below:
• VsUUID: This field contains the vserver UUID where FPolicy is enabled.
• PolicyName: This field contains the policy name in the vserver for which an external connection is
established with the External FPolicy server to provide file notification.
• SessionID: This is a unique identifier created by the storage appliance once a secure connection is
established with the External FPolicy server. The External FPolicy server must store the session_id to tag a connection for a policy. The storage appliance will use this session_id in case the connection is broken, and FSM re-establishes the session. The session_id is also useful for VIF movement within the same node.
• ProtVersions: This field contains the protocol version number. In the future, protocol handshake requests might contain multiple protocol versions, as sent by the storage appliance to the External FPolicy server. The External FPolicy server must return one protocol from the list of protocols provided in the Handshake Request.

File Notification Example after the Handshake:
"...."<?xml version="1.0"?><Header><NotfType>NEGO_REQ</NotfType><ContentLen>287</ContentLen><DataFormat>XML</DataFormat></Header>
<?xml version="1.0"?><Handshake><VsUUID>45228b37-6292-11ee-b5d1-000c29cdbe04</VsUUID><PolicyName>policy-test-flo</PolicyName><SessionId>d8ad84cc-79dd-11ee-b638-000c29cdbe04</SessionId><ProtVersion><Vers>1.0</Vers><Vers>1.1</Vers><Vers>1.2</Vers><Vers>2.0</Vers></ProtVersion></Handshake>."...h"<?xml version="1.0"?><Header><NotfType>NEGO_RESP</NotfType><ContentLen>234</ContentLen><DataFormat>XML</DataFormat></Header>
<?xml version="1.0"?><HandshakeResp><VsUUID>45228b37-6292-11ee-b5d1-000c29cdbe04</VsUUID><PolicyName>policy-test-flo</PolicyName><SessionId>d8ad84cc-79dd-11ee-b638-000c29cdbe04</SessionId><ProtVersion>1.2</ProtVersion></HandshakeResp>"...|"<?xml version="1.0"?><Header><NotfType>KEEP_ALIVE</NotfType><ContentLen>0</ContentLen><DataFormat>XML</DataFormat></Header>."...|"<?xml version="1.0"?><Header><NotfType>KEEP_ALIVE</NotfType><ContentLen>0</ContentLen><DataFormat>XML</DataFormat></Header>."...|"<?xml version="1.0"?><Header><NotfType>KEEP_ALIVE</NotfType><ContentLen>0</ContentLen><DataFormat>XML</DataFormat></Header>."...|"<?xml version="1.0"?><Header><NotfType>KEEP_ALIVE</NotfType><ContentLen>0</ContentLen><DataFormat>XML</DataFormat></Header>."...."<?xml version="1.0"?><Header><NotfType>SCREEN_REQ</NotfType><ContentLen>1038</ContentLen><DataFormat>XML</DataFormat></Header>
<?xml version="1.0"?><FscreenReq><ReqId>2822</ReqId><ReqType>SMB_OPEN</ReqType><NotfInfo><SmbOpenReq><CommonInfo><ProtCommonInfo><ClientIp>192.168.11.26</ClientIp><GenerationTime>1698970793791282</GenerationTime><UsrIdType>MAPPED_ID</UsrIdType><UsrContext><MappedId><Uid>0</Uid><WinSid>S-1-5-21-1595729341-2636328267-1414669823-1000</WinSid></MappedId></UsrContext><FileOwner><WinSid>S-1-5-32-544</WinSid></FileOwner><AccessPath><Path><PathNameType>WIN_NAME</PathNameType><PathName>\ntfs01</PathName></Path><Path><PathNameType>UNIX_NAME</PathNameType><PathName>/ntfs01</PathName></Path></AccessPath><VolMsid>2157674396</VolMsid><FileSize>4096</FileSize><NumHardLnk>2</NumHardLnk><IsOfflineAttr>0</IsOfflineAttr><FileType>DIR</FileType><IsSparse>0</IsSparse><IsDense>0</IsDense></ProtCommonInfo><DisplayPath>\\SVM0\ntfs01\</DisplayPath><ProtVer><MajorNum>3</MajorNum><MinorNum>1</MinorNum></ProtVer></CommonInfo><OpenAccmode>129</OpenAccmode><OpenSharemode>7</OpenSharemode><OpenOptions>0</OpenOptions></SmbOpenReq></NotfInfo></FscreenReq>.

Tests to Confirm Network Connection:
If possible, install Wireshark to monitor all the traffic between Splunk Enterprise and use the commands below.

	nc <client_ip> <client_port> < response.xml 

[server_ip_addr] curl ifconfig.me

Verify if you have correctly set the port number on the source host, and ensure that the port is both reachable and not blocked by the firewall.

nmap -p 1234 <ip>

Finally, confirm that the 'nc' utility is actively listening on the destination host.

netstat -ant | grep 1234

In addition, using “tcpdump” may be helpful to monitor the traffic.
tcpdump dst port 1234
tcpdump src <ip>


ONTAP FPolicy Steps:
Get ONTAP FPolicy Framework and set up running with Interfaces up.

Steps
1. After a few minutes from starting the machine, you receive a message to
log in to System Manager to complete cluster setup. This message includes an
IP address. 
Copy this IP address and paste it into your browser address bar to
open System Manager.
2. Ignore the message indicating that the partner node is not found.
3. Configure the single node cluster in System Manager. Follow the on-screen
prompts.

If an IP address is not automatically configured, complete the following steps.
Steps
1. Open the command prompt and execute “ifconfig”.
2. Pick an unused IP from the subnet of “IPv4 Address” 
3. Login to the console and execute the following command to configure the IP.

network interface create -vserver Default -lif mgmt_auto -role node-mgmt -
address <IP picked in step 2> -netmask <Netmask of IP picked in step2> -home-
port e0c

Example: (network interface create -vserver svm0 -lif svm0_01 -role data -data-protocol cifs,nfs,fcache -address 44.179.0.141 -netmask 255.255.252.0 -status-admin up)

4. Use the following URL to login to System Manager:
https://< IP picked in step 3>

PING: (ping -lif svm0_01 -vserver svm0 -destination 192.168.11.26)
ONTAP FPolicy Commands:

vserver fpolicy policy external-engine create -vserver svm0 -engine-name splunk-test -primary-servers 192.168.11.26 -port 1337 -extern-engine-type asynchronous -ssl-option no-auth -extern-engine-format xml


vserver fpolicy policy event create -vserver svm0 -event-name event-test-flo -volume-operation false -protocol cifs -file-operations open,read,write,rename,create

 
vserver fpolicy policy create -vserver svm0 -policy-name policy-test-flo -events event-test-flo -engine test-flo -is-mandatory false -allow-privileged-access no -is-passthrough-read-enabled false
















SVM TROUBLESHOOTING: 



fpolicy show

fpolicy enable -vserver fp -policy-name policy-test-flo -sequence-number 1 
fpolicy policy show -instance

vserver show
volume show
fpolicy policy scope create -vserver svm0 -policy-name policy-test-flo -volumes-to-include data
fpolicy enable -vserver svm0 -policy-name policy-test-flo -sequence-number 1

fpolicy show
fpolicy show-engine
fpolicy engine-connect -node fp-01 -policy-name policy-test-flo -server 192.168.11.26 -vserver svm0 
policy external-engine show

ping -lif svm0_01 -vserver svm0 -destination 192.168.11.26

show-engine
set d
show -instance
policy show -instance
fpolicy policy modify -vserver svm -policy-name policy-test-flo -engine splunk-test

disable -vserver svm0
disable -vserver svm0 -policy-name policy-test-flo
fpolicy policy modify -vserver svm0 -policy-name policy-test-flo -engine splunk-test 
enable -vserver svm0 -policy-name policy-test-flo -sequence-number 1

show-engine
engine-connect -node fp-01 -policy-name policy-test-flo -server 192.168.11.26 -vserver svm0 




Connect to SVM with the mount command using CIFS:
End User (Ubuntu User):
sudo mount -t cifs //192.168.10.246/ntfs01 /mnt/share_svm0_01 -o username=gurkan,password=passworde

cd /mnt/share_svm0_01 

ONTAP FPolicy Framework
cifs share show -vserver svm0
cifs users-and-groups show-domain-sid
cifs users-and-groups local-user show
cifs users-and-groups local-user set-password -user-name Administrator -vserver svm0
cifs users-and-groups local-group show
cifs users-and-groups local-user create -user-name gurkan -is-account-disabled false -vserver svm0
cifs users-and-groups local-group add-members -group-name BUILTIN\Administrators -member-names gurkan -vserver svm0


Successful Handshake
The image below is the confirmation of the handshake's success.

The image above shows a File Notification on the wire.
