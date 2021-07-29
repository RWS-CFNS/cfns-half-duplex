import serial.tools.list_ports
# https://fishandwhistle.net/post/2016/using-pyserial-pynmea2-and-raspberry-pi-to-log-nmea-output/

def connected_ports():
    list_ports = serial.tools.list_ports.comports(include_links=True)
    ports = []
    descs = []
    hwids = []
    for port, desc, hwid in sorted(list_ports):
        ports.append(port)
        descs.append(desc)
        hwids.append(hwid)
        print("{}: {} [{}]".format(port, desc, hwid))
    return ports, descs, hwids


connected_ports()