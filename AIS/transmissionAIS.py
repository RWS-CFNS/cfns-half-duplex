#!/usr/bin/env python3

import socket, time

DOS_EOL = "\x0D\x0A"
'''
DOS style end-of-line (<cr><lf>) for talking to AIS base stations
'''
EOL=DOS_EOL

HOST = '192.168.0.100'  # The server's hostname or IP address
PORT = 10111        # The port used by the server
addr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.send(b'!AIVDM,1,1,,A,10`lQ3hP000EfQ@N7REv4?wF25B4,0*23')
    #s.write("!AIBBM,1,1,0,2,8,04a9M>1@PU>0U>06185=08E99V1@E=4,0*7C".encode("utf-8"))
msg = "!AIBBM,1,1,0,2,8,04a9M>1@PU>0U>06185=08E99V1@E=4,0*7C".encode("utf-8")
s.connect((HOST,PORT))
while True:
    try:
        print("Writing to " + HOST)

        s.sendto(msg, addr)

        time.sleep(10)
        # ser_bytes = ser.readline()
        # print(ser_bytes)
    except:
        print("Keyboard Interrupt")
        s.close()
        break
