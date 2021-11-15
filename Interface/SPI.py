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

import spidev
from main import new_print

old_print = print
print = new_print

class SPI:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi_bus = 0
        self.spi_device = 0

    def get_spi_bus(self):
        return self.spi_bus

    def set_spi_bus(self, new_spi_bus):
        self.spi_bus = new_spi_bus

    def get_spi_device(self):
        return self.spi_device

    def set_spi_device(self, new_spi_device):
        self.spi_device = new_spi_device

    def init_spi(self, spi_bus, spi_device):
        self.spi_bus = spi_bus
        self.spi_device = spi_device
        self.spi.max_speed_hz = 1000000

    def open_spi(self):
        self.spi.open(self.spi_bus, self.spi_device)

    def close_spi(self):
        self.spi.close()

    def write_spi(self, data, type):
        # Write a single byte to address 80
        buff = []
        buff.append(data)
        buff.append(type)
        self.spi.writebytes([buff])
        print("data send")

    def read_spi(self):
        # Read 64 bytes from address 80
        msg = self.spi.readbytes(64)
        return msg
