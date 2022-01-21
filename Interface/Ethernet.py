'''
project: half-duplex, slimmer maken multiconnectivity modem
author: Alfred Espinosa Encarnación, Frank Montenij
Description: A class which represents an connection using Ethernet.
            
Changelog: Alfred created the file and Frank rewrote write and read. Also Frank added a helper function pad_msg_length.
'''

import socket
import json

"""
    pad the var msg_length to the padding size. 
    So that the message containing the msg_length has a fixed size of padding size.
"""
def pad_msg_length(padding_size, msg_length):
    msg_length = str(msg_length).encode()
    msg_length += b' ' * (padding_size - len(msg_length))
    return msg_length

class Ethernet:
    def __init__(self):
        self.ip_address = ""
        self.socket_port = 0
        self.sock = socket.socket()

    def get_ip_address(self):
        return self.ip_address

    def set_ip_address(self, new_ip_address):
        self.ip_address = new_ip_address

    def get_port(self):
        return self.socket_port

    def set_port(self, new_socket_port):
        self.socket_port = new_socket_port

    def init_socket(self, ip_address, socket_port):
        self.ip_address = ip_address
        self.socket_port = socket_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_socket(self):
        self.sock.connect((self.ip_address, self.socket_port))

    def close_socket(self):
        self.sock.close()

    """
        This method is used to send the confirmation_dict using the socket connection of this class.
        The method is also responsible for retrieving the reply message.
    """
    def write(self, dict, max_msg_length):
        buffer = json.dumps(dict)
        self.sock.send(pad_msg_length(max_msg_length, len(buffer)))
        self.sock.send(buffer.encode())
    
    def read_socket(self, max_msg_length):
        reply_length = self.sock.recv(max_msg_length).decode()
        reply = self.sock.recv(int(reply_length)).decode()
        reply = reply.replace("'", '"') # Change from single quotes to double quotes otherwise loads crashes
        reply = json.loads(reply)
        print("Client Sent : ", reply)

        return reply