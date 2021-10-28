import socket
import time

UDP_IP = "192.168.178.229"
UDP_PORT = 2947
MESSAGE = "!AIVDM,1,1,,A,10`lQ3hP000EfQ@N7REv4?wF25B4,0*23"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

while True:
    try:
        print("Writing to udp")
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        time.sleep(1)
        print("####### pycharm is listening #######")
        data = sock.recvfrom(2947)
        print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")

    except:
        print("Keyboard Interrupt")
        break
