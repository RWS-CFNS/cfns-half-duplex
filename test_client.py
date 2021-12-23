import socket
import json

max_msg_length = 10

def pad_msg_length(padding_size, msg_length):
    msg_length = str(msg_length).encode()
    msg_length += b' ' * (padding_size - len(msg_length))
    return msg_length

def setupSocket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.178.68", 8001))

    return client

def send_msg(msg, client):
    msg_length = pad_msg_length(max_msg_length, len(msg))

    client.send(msg_length)
    client.send(msg.encode())

def receive_msg(client):
    reply_length = int(client.recv(max_msg_length).decode())
    reply = client.recv(reply_length).decode()
    return reply

def test_receive():
    client = setupSocket()

    msg = json.dumps({"test": True})
    send_msg(msg, client)

    client.close()

def test_failed_receive():
    client = setupSocket()
    client.close()

def test_reply_interface():
    client = setupSocket()

    for _ in range(2):
        reply = receive_msg(client)
        print(reply)
        send_msg(reply, client)

    client.close()

def test_onboard_interface():
    client = setupSocket() 
    client.close()
    
    msg_list = [
        json.dumps({"request_type": "latest"}),
        json.dumps({"request_type": "by_category", "category": "other"}),
        json.dumps({"request_type": "test"}),
        json.dumps(["no", "dict"]),
        "no json",
        json.dumps({"request_type": "unknown"}),
        json.dumps({"incorrect": "format"}),
    ]

    for msg in msg_list:
        client = setupSocket()
        send_msg(msg, client)
        reply = receive_msg(client)
        print(reply)
        client.close()

def main():
    choice = input("what client do you want to use: ")

    if choice == "test_interface_receive":
        test_receive()
    elif choice == "test_interface_failed_receive":
        test_failed_receive()
    elif choice == "test_interface_reply":
        test_reply_interface() 
    elif choice == "test_onboard_interface":
        test_onboard_interface() 
    else:
        return

main()