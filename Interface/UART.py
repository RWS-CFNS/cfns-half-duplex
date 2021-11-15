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

import serial
from serial import Serial
import main

old_print = print
print = main.new_print

class UART:
    def __init__(self):
        self.port = ""
        self.baudrate = 0
        self.ser = Serial()

    def get_port(self):
        return self.port

    def set_port(self, new_port):
        self.port = new_port

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, new_baudrate):
        self.baudrate = new_baudrate

    def init_serial(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(
            port=self.port, baudrate=self.baudrate, bytesize=8, stopbits=serial.STOPBITS_ONE
        )
        self.ser.flush()

    def check_connection_rs232(self):
        print("Serial is open: " + str(self.ser.isOpen()))
        return self.ser.isOpen()

    def open_rs232(self):
        self.ser.open()
        return self.ser.isOpen()

    def close_rs232(self):
        self.ser.close()
        return self.ser.isOpen()

    def write_rs232(self, msg):
        try:
            self.ser.write(str(msg).encode("utf-8"))  # "!AIBBM,1,1,0,2,8,04a9M>1@PU>0U>06185=08E99V1@E=4,0*7C"
            print("UART data send for acknowledgement: ", msg)
        except:
            print("Could not send by UART")
            pass

    def read_rs232(self):
        msg = self.ser.readline()
        return msg
