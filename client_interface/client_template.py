import socket
import json

max_msg_length = 10

def pad_msg_length(padding_size, message_length):
    message_length = str(message_length).encode()
    message_length += b' ' * (padding_size - len(message_length))
    return message_length

# Connect to interface
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.178.68", 8001))

# Build message
message = json.dumps({"request_type": "latest"}).encode()
message_length = pad_msg_length(max_msg_length, len(message))

# Send message 
client.send(message_length)
client.send(message)

# Receive reply
reply_length = int(client.recv(max_msg_length).decode())
reply = client.recv(reply_length).decode()

# Extract reply
reply_dict = json.loads(reply)
print(reply)