[server_input://<name>]
index = An index to save File Notifications as XML.  Default: default
Policy_Name = FPolicy File Policy Name. Please see the 'vserver fpolicy policy show' output. (Use the same Policy Name for a successful handshake with FPolicy. )
sa_cert = Upload server side SSL certificate.  Default: empty
sa_key = Upload server side SSL Key.  Default: empty
Server_IP = IP address for the Add-on as an External Server. Please see the external engine settings of FPolicy. (Use the external IP of the Splunk instance.)  Default: 0.0.0.0
Server_Port = Port number for the Add-on as an External Server. Please see the external engine settings of FPolicy. (Use an unused port number for each input.)  Default: 1337
sourcetype = A unique sourcetype for the data.
use_ssl = Check if you want to use SSL for ONTAP connection.  Default: False
