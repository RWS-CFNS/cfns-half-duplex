#!/usr/bin/python
from Interface.Interface import Interface


class Device(Interface):
    def __init__(self, name, branch, model, interface_type, technology):
        super().__init__(interface_type)
        self.name = name
        self.branch = branch
        self.model = model
        self.technology = technology

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

    def get_interface(self):
        return self.interface_type

    def set_interface(self, new_interface):
        self.interface_type = new_interface
    
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

