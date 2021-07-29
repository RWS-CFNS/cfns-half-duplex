import socket
import json


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

    def init_socket(self, IP, PORT):
        self.ip_address = IP
        self.socket_port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_socket(self):
        self.sock.connect((self.ip_address, self.socket_port))

    def close_socket(self):
        self.sock.close()

    def write_socket(self, data):

        buffer = json.dumps({"ack": data[0], "msg": data[1]})

        self.sock.send(buffer.encode())
        reply = self.sock.recv(1024)

        print("Client Sent : ", reply)

    def read_socket(self):
        data, addr = self.sock.recvfrom(4096)
        return data, addr
