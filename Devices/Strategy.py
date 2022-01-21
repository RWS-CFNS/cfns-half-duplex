'''
project: half-duplex, slimmer maken multiconnectivity modem
author: Alfred Espinosa Encarnación, Frank Montenij
Description: A class which represents the different strategies for communicating with physical devices.
            
Changelog: Frank created the file, but used Alfred his code in the communicate methods for the classes: I2CStrategy, SPIStrategy and AISStrategy.
'''

from abc import ABC, abstractmethod
import aisutils
import time

class Strategy(ABC):
    def __init__(self, interface):
        self.interface = interface

    @abstractmethod
    def communicate(self, data) -> bool:
        """Subclasses need to implement this method. It must returns a bool value."""

class I2CStrategy(Strategy):
    """Class to define how to communcicate with an I2C interface."""
    
    def __init__(self, interface):
        super().__init__(interface)
        self.amount_of_bytes_to_read = 2

    """
        Converts the data to a list, because the I2C class requires the data in a list format.
        If the data_list is one item long with that item being a one it means that it ask the device if it has reach or not.
        The device will return that answer at the first place of reply. And the answer for the confirmation at the second place of reply. 
    """
    def communicate(self, data):
        try:
            data_list = self.data_dict_to_list(data)
            if not data_list:
                return False
            
            self.interface.write(data_list)

            if len(data_list) == 1 and data_list[0] == 1: 
                # Has_reach reply
                # Sleep for 10 seconds, because getting reach can take up to 10 seconds.
                time.sleep(10)

                reply = self.interface.read_i2c(self.amount_of_bytes_to_read)[0]
            else: 
                # DAB confirmation reply
                reply = self.interface.read_i2c(self.amount_of_bytes_to_read)[1]
            return reply if reply else False 
        except OSError as e:
            print(e)
            return False
        except OverflowError as e:
            print(e)
            return False
    
    """
        Converts data dict to data list. I2C works with byte lists.
    """
    def data_dict_to_list(self, data):
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            data_list = [value for key, value in data.items() if not key == "dab_id"]

            if "dab_id" in data:
                dab_id_bytes = data.get("dab_id").to_bytes(2, 'little')
                # the i2c device expects the dab_id at the first place as two bytes at two seperate places in little endian order.
                data_list.insert(0,dab_id_bytes[0]) 
                data_list.insert(1,dab_id_bytes[1])

            return data_list
        else:
            return False


class SPIStrategy(Strategy):
    """Class to define how to communcicate with a SPI interface."""
    
    def __init__(self, interface):
        super().__init__(interface)

    def communicate(self, data):
        try:
            # The code is commented because there is no device that uses the SPIStrategy yet. So the values are not known and implementation could cause crashes
            # # new_spi_bus = 
            # # new_spi_device = 
            # self.interface.set_spi_bus(new_spi_bus)
            # self.interface.set_spi_device(new_spi_device)
            # self.interface.open_spi()
            # self.interface.write(data.get("dab_id"), data.get("message_type"))

            # reply = self.interface.read_spi()
            # self.interface.close_spi()
            # return True if reply else False 
            return False
        except Exception as e: # no specific exception defined, becaus spi has not been implemented for any of the used technologies. Therefore there is no specific exception knownspi.clo
            print(e)
            return False

class AISStrategy(Strategy):
    """Class to define how with communicate to an AIS device."""
    
    def __init__(self, interface):
        super().__init__(interface)

    def communicate(self, data):
        try:
            if data.get("message_type") == 4:
                msg = '  ACK:' + str(data.get("dab_id")) + ',MSG:' + str(data.get("message_type")) + ',RSSI:' + str(data.get("dab_signal")) + ',SNR:-1'
            else:
                msg = '  ACK:' + str(data.get("dab_id")) + ',MSG:' + str(data.get("message_type")) + ''
            
            # Convert msg string to nmea string
            aisBits = aisutils.BitVector.BitVector(textstring=msg)
            payloadStr, pad = aisutils.binary.bitvectoais6(aisBits)  # [0]
            buffer = aisutils.nmea.bbmEncode(1, 1, 0, 1, 8, payloadStr, pad, appendEOL=False)
            self.interface.write(buffer)
            return True
        except Exception as e:
            print(e)
            return False

class EthernetStrategy(Strategy):
    """Class to define how to communcicate with an ethernet interface."""

    def __init__(self, interface):
        super().__init__(interface)
    
    def communicate(self, data):
        try:
            # This is the max size a message containing the length of the message can be.
            max_msg_length = 10 

            reply = {"reply": False}
            self.interface.init_socket(self.interface.ip_address, self.interface.socket_port)
            with self.interface.sock:
                self.interface.connect_socket() 
                self.interface.write(data, max_msg_length)
                reply = self.interface.read_socket(max_msg_length)
                
            # If 'reply' is in reply and false return False. If 'reply' is not in reply or not False return reply.
            if reply.get('reply') == False:
                return False
            else:
                return reply
        except Exception as e:
            print(e)
            return False