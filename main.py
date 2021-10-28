#
#    CFNS - Rijkswaterstaat CIV, Delft © 2020 - 2021 <cfns@rws.nl>
#
#    Copyright 2020 - 2021 Alfred Espinosa Encarnación <alfred.espinosaencarnacion@rws.nl>
#
#    This file is part of cfns-half-duplex
#
#    cfns-half-duplex is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    cfns-half-duplex is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with cfns-half-duplex. If not, see <https://www.gnu.org/licenses/>.
#

import os
import sys
import argparse
import csv
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from aisutils import nmea
from aisutils import BitVector
from aisutils import binary


from Device import Device
from Folder import Folder
from File import File
import time


class Monitor(PatternMatchingEventHandler):

    def __init__(self, folder):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], ignore_directories=True, case_sensitive=False)
        self.folder = folder
        self.devices = []

    def on_created(self, event):
        print(event.src_path, event.event_type)
        time.sleep(1)

        # Save new DAB+ message as File object
        new_file = File(str(event.src_path).replace(self.folder.path, ""))

        # Add new DAB+ message to the Folder object
        self.folder.files.append(new_file)
        new_file.set_lines(self.folder.path)

        # Get DAB+ ID & Message Type
        dab_id = new_file.get_dab_id()
        message_type = new_file.get_message_type()

        for line in new_file.get_lines():
            print(line)

        data = []
        if message_type == 4:
            data.append(get_dab_signal())
        self.acknowledge(dab_id, message_type, data)

    def acknowledge(self, dab_id, message_type, data):
        for d in self.devices:
            if d.interface_type == 0:
                try:
                    if message_type == 4:
                        msg = '  ACK:' + str(dab_id) + ',MSG:' + str(message_type) + ',RSSI:' + str(data[0]) + ',SNR:-1'
                        aisBits = BitVector.BitVector(textstring=msg)
                        payloadStr, pad = binary.bitvectoais6(aisBits)  # [0]
                        buffer = nmea.bbmEncode(1, 1, 0, 1, 8, payloadStr, pad, appendEOL=False)
                        d.rs232.write_rs232(buffer)
                    else:
                        msg = '  ACK:' + str(dab_id) + ',MSG:' + str(message_type) + ''
                        aisBits = BitVector.BitVector(textstring=msg)
                        payloadStr, pad = binary.bitvectoais6(aisBits)  # [0]
                        buffer = nmea.bbmEncode(1, 1, 0, 1, 8, payloadStr, pad, appendEOL=False)
                        d.rs232.write_rs232(buffer)

                except ("There is no connection with: %s" % d.name):
                    print("Could not send with: %s" % d.name)
                    pass
            elif d.interface_type == 1:
                try:
                    d.i2c.write_i2c(dab_id, message_type, data)
                except ("There is no connection with: %s" % d.name):
                    print("Could not send with: %s" % d.name)
                    pass
            elif d.interface_type == 2:
                try:
                    d.ethernet.init_socket(d.ethernet.ip_address, d.ethernet.socket_port)
                    d.ethernet.connect_socket()
                    d.ethernet.write_socket([dab_id, message_type])
                    d.ethernet.close_socket()
                except ("There is no connection with: %s" % d.name):
                    print("Could not send with: %s" % d.name)

                    pass
            elif d.interface_type == 3:
                try:
                    d.spi.write_spi(dab_id, message_type)
                except ("There is no connection with: %s" % d.name):
                    print("Could not send with: %s" % d.name)
                    pass


def execute():
    # create parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument("devices")
    parser.add_argument("folder")

    # parse the arguments
    args = parser.parse_args()

    # Create Folder object with path of folder
    dab_folder = Folder(os.path.expanduser(args.folder))

    # Assign folder to be monitored
    event_handler = Monitor(dab_folder)
    observer = Observer()
    observer.schedule(event_handler, path=event_handler.folder.path, recursive=True)

    # Assign list of devices attached to the system
    event_handler.devices = attach_devices(args.devices)

    observer.start()
    print("Monitoring started")
    try:
        while (True):
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring Stopped")
    observer.join()


def get_dab_signal():
    return 20


def attach_devices(csv_parameter):
    listed_devices = []

    try:
        with open(csv_parameter, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1

                if int(row["interface_type"]) == 0:
                    print(row["name"])
                    ais = Device(row["name"], row["branch"], row["model"], int(row["interface_type"]))
                    ais.rs232.init_serial(row["address"], int(row["setting"]))
                    listed_devices.append(ais)

                if int(row["interface_type"]) == 1:
                    print(row["name"])
                    lora = Device(row["name"], row["branch"], row["model"], int(row["interface_type"]))
                    lora.i2c.init_i2c(int(row["address"]))
                    listed_devices.append(lora)

                if int(row["interface_type"]) == 2:
                    print(row["name"])
                    lan = Device(row["name"], row["branch"], row["model"], int(row["interface_type"]))
                    lan.ethernet.init_socket(row["address"], int(row["setting"]))
                    listed_devices.append(lan)

                if int(row["interface_type"]) == 3:
                    print(row["name"])
                    lora2 = Device(row["name"], row["branch"], row["model"], int(row["interface_type"]))
                    lora2.spi.init_spi(int(row["address"]), int(row["setting"]))
                    listed_devices.append(lora2)
                line_count += 1
            print(f'Processed {line_count} lines.')

        if line_count > 1:
            return listed_devices
        else:
            print("No devices are listed. Configure {} and execute the program again".format(csv_parameter))
            sys.exit()
    except RuntimeError:
        print("Could not open list with devices")


if __name__ == "__main__":

    try:
        execute()
    except RuntimeError:
        print("Could not execute programm")
