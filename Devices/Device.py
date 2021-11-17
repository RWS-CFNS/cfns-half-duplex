#!/usr/bin/python
from Devices.Strategy import AISStrategy, EthernetStrategy, StandardStrategy
from Interface.I2C import I2C
from Interface.Ethernet import Ethernet
from Interface.UART import UART
from Interface.SPI import SPI

class Device:
    def __init__(self, name, branch, model, interface_type, technology, priority):
        self.interface = self.set_interface(interface_type)
        self.name = name
        self.branch = branch
        self.model = model
        self.technology = technology
        self.priority = priority
        self.strategy = self.set_strategy_based_on_interface_type(interface_type)
    
    def set_strategy_based_on_interface_type(self, interface_type):
        if interface_type == 0:
            self.strategy = AISStrategy()
        elif interface_type == 1:
            self.strategy = StandardStrategy()
        elif interface_type == 2:
            self.strategy = EthernetStrategy()
        elif interface_type == 3:
            self.strategy = StandardStrategy()
        
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def get_strategy(self):
        return self.strategy

    def set_interface(self, interface_type):
        """
        Interface value (interface_type) given by the Device-object
        must be equal to the following interfaces to make use of the implementation
        
        UART                =   0 
        I2C                 =   1
        Socket (Ethernet)   =   2
        SPI                 =   3
        """
        if interface_type == 0:
            return UART()
        elif interface_type == 1:
            return I2C()
        elif interface_type == 2:
            return Ethernet()
        elif interface_type == 3:
           return SPI()

    def get_interface(self):
        return self.interface
        
    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_branch(self):
        return self.branch

    def set_branch(self, new_branch):
        self.branch = new_branch

    def get_model(self):
        return self.model

    def set_model(self, new_model):
        self.model = new_model
    
    def get_technology(self):
        return self.technology
    
    def set_technology(self, new_technology):
        self.technology = new_technology


'''
AIS device with interface
'''
# name, branch, model, port, type
#p1 = Device("AIS Transponder1", "True Heading", "AIS Base Station", 0)
# p1.setport("/dev/ttyUSB0")
# p1.init_serial(38400, 8, serial.STOPBITS_ONE)
# p1.check_connection_rs232()
#p1.init_i2c()
#p1.list_i2c()
#p1.close_rs232()
# p1.intf.setport("/dev/ttyUSB0")
# p1.intf.init_serial(38400, 8, serial.STOPBITS_ONE)
# p1.intf.checkconnection()
# msg = p1.encode_BBM(0)
#p1.intf.write(msg)


# aisin = interf.Interface(p1.name, p1.type)
# aisin.setport("/dev/ttyUSB0")
# aisin.init_serial(38400, 8, serial.STOPBITS_ONE)
# print(aisin.checkconnection())
# print(aisin.read())

#p1.getname()