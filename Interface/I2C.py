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

from smbus2 import SMBus, i2c_msg # type: ignore this line

class I2C:
    def __init__(self):
        self.target_address = 0
        self.bus = SMBus()

    def get_target_address(self): 
        return self.target_address

    def init_i2c(self, target_address):
        self.target_address = target_address
        self.bus = SMBus(1)

    def list_i2c(self):
        for device in range(128):
            try:
                msg = i2c_msg.write(device, [64])
                self.bus.i2c_rdwr(msg)
                self.bus.read_byte(device)
                print(device)
            except:
                print("No device connected to bus")
                pass

    def write(self, data): 
        print(data, type(data))       
        msg = i2c_msg.write(self.target_address, data)
        self.bus.i2c_rdwr(msg)
        print("I2C data send for acknowledgement: ", data)

    def read_i2c(self, amount_of_bytes):
        reply = i2c_msg.read(self.target_address, amount_of_bytes)
        self.bus.i2c_rdwr(reply)
        return list(reply)

