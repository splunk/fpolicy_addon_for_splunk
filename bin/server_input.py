import import_declare_test

import sys
import json

from splunklib import modularinput as smi

import os
import traceback
import requests
from splunklib import modularinput as smi
from solnlib import conf_manager
from solnlib import log
from solnlib.modular_input import checkpointer
from splunktaucclib.modinput_wrapper import base_modinput  as base_mi 

import threading
import socket
import re
import struct
import xml.etree.ElementTree as ET
import json

class ClientHandler(threading.Thread):
    def __init__(self, helper, ew, client_sock, client_addr):
        super().__init__()
        self.helper = helper
        self.ew = ew
        self.client_sock = client_sock
        self.client_addr = client_addr

    def run(self):

        base_segment_length = 345
        base_message_length = 219
        policy_name = self.helper.get_arg("Policy_Name")
        name_length = len(policy_name)
        message_length = base_message_length + name_length

        # get input values
        index=self.helper.get_arg("index")
        sourcetype=self.helper.get_arg("account")['name']
        host = self.helper.get_arg("Server_IP")
        port = int(self.helper.get_arg("Server_Port"))

        self.helper.log_info(f"\n\n [INFO] Connection accepted from {self.client_addr} [FPolicy : "+policy_name+"] \n\n")

        while True:
            #inner_loop_count = inner_loop_count + 1
            raw_data = ""
            hex_data = ""

            try:
                # receive byte data
                hex_data = self.client_sock.recv(1024)
            except Exception as e:
                self.helper.log_error('\n\n [ERROR] Get exception when client_sock.recv(1024). '+ str(e)+" [FPolicy : "+policy_name+"] \n\n")

            if hex_data == "": 
                self.helper.log_info(f"\n\n [INFO] Loop exit. [FPolicy : "+policy_name+"] \n\n")
                break

            unk_hex_data = hex_data[:6]

            # first 6 chars are hexadecimal not binary
            if hex_data!= "": 
                self.helper.log_info(f"\n\n [INFO] hex_data received. (hex_data!= "") [FPolicy : "+policy_name+"] \n\n")
                #raw_data = hex_data[6:]
                raw_data = hex_data[6:-1]
                
            try:
                #check for handshake
                #data = raw_data.decode()
                data = ''  # an empty string to store decoded chars

                for byte in raw_data:
                    try:
                        # byte is treated as byte, not an int
                        byte = bytes([byte])
                        # decode each byte 
                        decode_char = byte.decode()
                        data += decode_char
                    except UnicodeDecodeError:
                        self.helper.log_error("\n\n [ERROR] (UnicodeDecodeError) data: \n "+ str(data)+" [FPolicy : "+policy_name+"] \n\n")
                        # error handling for this byte
                        data += '.'  # undecodable characters as '.' similar to wire shark
            except Exception as err:
                self.helper.log_error('\n\n [ERROR] Get exception when byte.decode(). '+ str(e)+" [FPolicy : "+policy_name+"] \n\n")
                data_tmp = raw_data

            # here edit find the <SessionId>
            tag_start = "<SessionId>"
            tag_end = "</SessionId>"
            pattern = f'{re.escape(tag_start)}(.*?)\s*{re.escape(tag_end)}'
            match_SessionId = re.search(pattern, data)
            # here edit find the <VsUUID>
            tag_start = "<VsUUID>"
            tag_end = "</VsUUID>"
            pattern = f'{re.escape(tag_start)}(.*?)\s*{re.escape(tag_end)}'
            match_VsUUID = re.search(pattern, data)

            if (match_VsUUID and match_SessionId):
                # here edit find the <NotfType>
                tag_start = "<NotfType>"
                tag_end = "</NotfType>"
                pattern = f'{re.escape(tag_start)}(.*?)\s*{re.escape(tag_end)}'
                match_NotfType = re.search(pattern, data)
                result_NotfType = match_NotfType.group(1)
                self.helper.log_info("\n\n [INFO] NotfType : {}".format(result_NotfType) + " [FPolicy : "+policy_name+"] \n\n")

            if (match_VsUUID and match_SessionId and result_NotfType == 'NEGO_REQ'):
                result_SessionId = match_SessionId.group(1)
                #self.helper.log_info("\n\n [INFO] SessionId : {}".format(result_SessionId) +" [FPolicy : "+policy_name+"] \n\n")
                result_VsUUID = match_VsUUID.group(1)
                #self.helper.log_info("\n\n [INFO] VsUUID : {}".format(result_VsUUID) + " [FPolicy : "+policy_name+"] \n\n")

                header_resp = ("<?xml version=\"1.0\"?><Header><NotfType>NEGO_RESP</NotfType><ContentLen>"+str(message_length)+"</ContentLen><DataFormat>XML</DataFormat></Header>")
                # send a header
                #self.helper.log_info("\n\n [INFO] Header to send : {}".format(header_resp)+" [FPolicy : "+policy_name+"] \n\n")
                # SessionId and VsUUID should change only
                handshake_resp = ("<?xml version=\"1.0\"?><HandshakeResp><VsUUID>" + ("%s" % (result_VsUUID)) + "</VsUUID><PolicyName>"+policy_name+"</PolicyName><SessionId>"+("%s" % (result_SessionId))+"</SessionId><ProtVersion>1.2</ProtVersion></HandshakeResp>")

                try:
                    # send a response
                    #self.helper.log_info("\n\n [INFO] Response to send : {}".format(header_resp+"\n\n"+handshake_resp)+" [FPolicy : "+policy_name+"] \n\n")
                    #the size of the input string
                    size = len(header_resp+"\n\n"+handshake_resp)
                    #self.helper.log_info("\n\n [INFO] Size of the segment : "+str(size) +" [FPolicy : "+policy_name+"] \n\n")
                    # the size in big-endian format
                    size_bytes = struct.pack('>I', size)
                    # the size bytes and the original string
                    to_send ="\"".encode('utf-8') + size_bytes + "\"".encode('utf-8') +(header_resp+"\n\n"+handshake_resp).encode('utf-8')

                    # the results
                    self.client_sock.send(to_send)
                    complete = to_send
                    self.helper.log_info("\n\n [INFO] Complete the segment sent below  [FPolicy : "+policy_name+"] : \n")
                    self.helper.log_info((complete))
                    #self.helper.log_info("\n [INFO] Please confirm if handshake is/was successful by using FPolicy console. [FPolicy : "+policy_name+"] \n\n")
                except Exception as err:
                    self.helper.log_error('\n\n [ERROR] Get exception when client_sock.send(to_send). '+ str(e)+" [FPolicy : "+policy_name+"] \n\n")

            if raw_data != "": 
                self.helper.log_info(f"\n\n [INFO] Data to write {index} index: {data}  [FPolicy : "+policy_name+"] \n\n")

                sourcetype=  policy_name  + "://" + self.helper.get_input_stanza_names()
                event = self.helper.new_event(source=policy_name, index=index, sourcetype=sourcetype , data=data)

                try:
                    self.ew.write_event(event)
                except Exception as e:
                    self.helper.log_error('\n\n [ERROR] Get exception when ew.write_event(event). '+ str(e)+" [FPolicy : "+policy_name+"] \n\n")

                self.helper.log_info("\n\n [INFO] Event Inserted in XML format. \n source="+policy_name+", index="+index+", sourcetype="+sourcetype+" , data="+data+" [FPolicy : "+policy_name+"] \n\n")

                self.helper.log_info(f"\n\n [INFO] Inner loop. [FPolicy : "+policy_name+"] \n\n")

            elif raw_data == "": 
                self.helper.log_info(f"\n\n [INFO] Loop exit. [FPolicy : "+policy_name+"] \n\n")
                break
            else: 
                self.helper.log_info(f"\n\n [INFO] Loop exit. [FPolicy : "+policy_name+"] \n\n")
                break

        self.helper.log_info(f"\n\n [INFO] ClientHandler END. [FPolicy : "+policy_name+"] \n\n")

        #Connection from {self.address} closed
        #self.client_socket.close()

bin_dir  = os.path.basename(__file__)
app_name = os.path.basename(os.path.dirname(os.getcwd()))

class ModInputSERVER_INPUT(base_mi.BaseModInput): 

    def __init__(self):
        use_single_instance = False
        super(ModInputSERVER_INPUT, self).__init__(app_name, "server_input", use_single_instance) 
        self.global_checkbox_fields = None

    def get_scheme(self):
        scheme = smi.Scheme('server_input')
        scheme.description = 'server_input'
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False

        scheme.add_argument(
            smi.Argument(
                'name',
                title='Name',
                description='Name',
                required_on_create=True
            )
        )
        scheme.add_argument(
            smi.Argument(
                'account',
                required_on_create=True,
            )
        )
        
        return scheme

    def validate_input(self, definition):
        """validate the input stanza"""
        """Implement your own validation logic to validate the input stanza configurations"""
        pass

    def get_app_name(self):
        return "app_name" 

    def handle_conn(self, helper, ew, client_socket, address):
        print(f"Accepted connection from {address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data from {address}: {data.decode('utf-8')}")
            client_socket.sendall(data)

        print(f"Connection from {address} closed")
        client_socket.close()

    def collect_events(helper, ew):
        #Start the Add-on Server to listen to handshake requests and file events.

        base_segment_length = 345
        base_message_length = 219
        policy_name = helper.get_arg("Policy_Name")
        name_length = len(policy_name)
        message_length = base_message_length + name_length

        # get input values
        index=helper.get_arg("index")
        sourcetype=helper.get_arg("account")['name']
        host = helper.get_arg("Server_IP")
        port = int(helper.get_arg("Server_Port"))

        # socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket
        sock.bind((host, port))
        sock.listen(5)
        # listen for five connection at a time
        helper.log_info(f"\n\n [INFO] Socket on {host}:{port} [FPolicy : "+policy_name+"] \n\n")

        while True:

            # wait for the first connection
            helper.log_info(f"\n\n [INFO] Listening... [FPolicy : "+policy_name+"] \n\n")

            while True:
                client_sock, client_addr = sock.accept()

                conn_handler = ClientHandler(helper, ew, client_sock, client_addr)
                conn_handler.start()

    def get_account_fields(self):
        account_fields = []
        return account_fields


    def get_checkbox_fields(self):
        checkbox_fields = []
        return checkbox_fields


    def get_global_checkbox_fields(self):
        if self.global_checkbox_fields is None:
            checkbox_name_file = os.path.join(bin_dir, 'global_checkbox_param.json')
            try:
                if os.path.isfile(checkbox_name_file):
                    with open(checkbox_name_file, 'r') as fp:
                        self.global_checkbox_fields = json.load(fp)
                else:
                    self.global_checkbox_fields = []
            except Exception as e:
                self.log_error('\n\n [ERROR] Get exception when loading global checkbox parameter names. '+ str(e)+" \n\n")
                self.global_checkbox_fields = []
        return self.global_checkbox_fields

if __name__ == '__main__':
    exit_code = ModInputSERVER_INPUT().run(sys.argv)
    sys.exit(exit_code)


