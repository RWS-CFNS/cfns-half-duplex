#!/usr/bin/python
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
