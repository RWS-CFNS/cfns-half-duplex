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

from .I2C import I2C
from .Ethernet import Ethernet
from .UART import UART
from .SPI import SPI


class Interface:
    def __init__(self, interface_type):

        self.interface_type = interface_type

        """
        Interface value (interface_type) given by the Device-object
        must be equal to the following interfaces to make use of the implementation
        
        UART                =   1
        I2C                 =   2
        Socket (Ethernet)   =   3
        SPI                 =   4
        """
        if self.interface_type == 0:
            self.rs232 = UART()
        elif self.interface_type == 1:
            self.i2c = I2C()
        elif self.interface_type == 2:
            self.ethernet = Ethernet()
        elif self.interface_type == 3:
            self.spi = SPI()

    def get_rs232_settings(self):
        return vars(self.rs232)

    def get_i2c_settings(self):
        return vars(self.i2c)

    def get_ethernet_settings(self):
        return vars(self.ethernet)

    def get_spi_settings(self):
        return vars(self.spi)
