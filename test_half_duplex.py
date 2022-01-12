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

import time
import unittest
from Category import Category
from Devices.Strategy import AISStrategy, I2CStrategy
from Interface.Ethernet import Ethernet
from Interface.I2C import I2C
from Interface.SPI import SPI
from Interface.UART import UART
from Status import Status

from File import File
from Folder import Folder
from Devices.Device import Device
from main import Monitor, attach_devices

''''
project: Half-Duplex
author: Alfred Espinosa Encarnación
date: 30-03-2021, 11-11-2021

Description: Testing method to test the functionalities of Half-Duplex. The class MyTestCase has been written by Alfred.

WERKT NIET MEER!
'''

class MyTestCase(unittest.TestCase):
    def test_file(self):

        # expected values when reading from dab+ message "bb.txt"
        assess_dab_id = 68
        assess_message_type = 2
        asesss_category = Category.OTHER
        assess_latitude = 52.6525
        assess_longitude = 4.7448
        
        # read the data from dab+ message
        test_filename = "bb.txt"
        test_path = "correct/"
        test_file = File(test_filename)
        test_file.set_lines(test_path)
        test_file.set_information()

        # assign data from dab+ message to variables
        test_dab_id = test_file.get_dab_id()
        test_message_type = test_file.get_message_type()
        test_category = test_file.get_category()
        test_latitude, test_longitude = test_file.get_coordinates()

        # check if the data from dab+ message equals to the expected data
        self.assertEqual(assess_dab_id, test_dab_id)
        self.assertEqual(assess_message_type, test_message_type)
        self.assertEqual(asesss_category, test_category)
        self.assertEqual(assess_latitude, test_latitude)
        self.assertEqual(assess_longitude, test_longitude)

    def test_folder(self):
        test_path = "correct/"
        test_folder = Folder(test_path)

        result_path = test_folder.get_path()
        test_folder.set_path("newpath/")
        result_new_path = test_folder.get_path()

        test_filename = "bb.txt"
        test_file = File(test_filename)
        test_folder.files.append(test_file)
        result_files = test_folder.get_list_files()

        self.assertEqual("correct/", result_path)
        self.assertEqual("newpath/", result_new_path)
        self.assertEqual(test_file, result_files[0])

    def test_device(self):
        test_device_instance = Device("AIS Transponder1", "True Heading", "AIS Base Station", "AIS", 0)
        test_device_instance.set_strategy(AISStrategy(UART()))

        result_name = test_device_instance.get_name()
        result_branch = test_device_instance.get_branch()
        result_model = test_device_instance.get_model()
        result_technology = test_device_instance.get_technology()
        result_priority = test_device_instance.get_priority()
        result_strategy = test_device_instance.get_strategy()

        self.assertEqual("AIS Transponder1", result_name)
        self.assertEqual("True Heading", result_branch)
        self.assertEqual("AIS Base Station", result_model)
        self.assertEqual("AIS", result_technology)
        self.assertEqual(0, result_priority)
        self.assertTrue(isinstance(result_strategy, AISStrategy))

        test_device_instance.set_name("test_name")
        test_device_instance.set_branch("python_unit")
        test_device_instance.set_model("PU-00")
        test_device_instance.set_technology("python")
        test_device_instance.set_priority(3)
        test_device_instance.set_strategy(I2CStrategy(I2C()))

        new_result_name = test_device_instance.get_name()
        new_result_branch = test_device_instance.get_branch()
        new_result_model = test_device_instance.get_model()
        new_result_technology = test_device_instance.get_technology()
        new_result_priority = test_device_instance.get_priority()
        new_result_strategy = test_device_instance.get_strategy()

        self.assertEqual("test_name", new_result_name)
        self.assertEqual("python_unit", new_result_branch)
        self.assertEqual("PU-00", new_result_model)
        self.assertEqual("python", new_result_technology)
        self.assertEqual(3, new_result_priority)  
        self.assertTrue(isinstance(new_result_strategy, I2CStrategy))

    def test_rs232(self):
        test_interface = UART()
        #test_rs232.init_serial("/dev/ttyUSB0", 115200)
        test_interface.set_port("/dev/ttyUSB0")
        test_interface.set_baudrate(38400)
        result_port = test_interface.get_port()
        result_baudrate = test_interface.get_baudrate()

        self.assertEqual("/dev/ttyUSB0", result_port)
        self.assertEqual(38400, result_baudrate)

        self.assertEqual(False, test_interface.close_rs232())

    def test_i2c(self):
        test_interface = I2C()
        test_interface.init_i2c(4)
        self.assertEqual(4, test_interface.get_target_address())

    def test_ethernet(self):
        test_interface = Ethernet()
        test_interface.init_socket("192.168.0.101", 1234)

        self.assertEqual("192.168.0.101", test_interface.get_ip_address())
        self.assertEqual(1234, test_interface.get_port())
        test_interface.close_socket()


    def test_spi(self):
        test_interface = SPI()
        test_interface.init_spi(0, 1)

        self.assertEqual(0, test_interface.get_spi_bus())
        self.assertEqual(1, test_interface.get_spi_device())

    def test_acknowledge(self):
        # Prepare the monitor
        test_folder = Folder("./correct")
        test_monitor = Monitor(test_folder)
        
        # Fills the list of devices with one device so choose device is not necessary
        test_monitor.devices = attach_devices("devices.csv") 
        test_device_instance_list = test_monitor.devices

        # Fill the folder with test files 
        test_file1 = File("test1")
        test_file1.dab_id = 67
        test_file1.message_type = 4
        test_file2 = File("test2")
        test_file2.dab_id = 100
        test_file2.message_type = 2
        test_file3 = File("test3")
        test_file3.dab_id = 6
        test_file3.message_type = 1
        test_monitor.folder.files = [test_file1, test_file2, test_file3]

        # Create the data to send
        time_of_arrival = time.time()
        data1 = test_monitor.create_confirmation_dict(test_file1.get_dab_id(), test_file1.get_message_type(), time_of_arrival)
        data2 = test_monitor.create_confirmation_dict(test_file2.get_dab_id(), test_file2.get_message_type(), time_of_arrival)
        data3 = test_monitor.create_confirmation_dict(test_file3.get_dab_id(), test_file3.get_message_type(), time_of_arrival)

        # Here the tests will be executed and determined if they were a succes or not
        expected_result = Status.CONFIRMED

        test_monitor.acknowledge(data1, test_device_instance_list)
        file1_after_test = test_monitor.folder.find_file_by_dab_id(test_file1.get_dab_id())
        self.assertEqual(file1_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data2, test_device_instance_list)
        file2_after_test = test_monitor.folder.find_file_by_dab_id(test_file2.get_dab_id())
        self.assertEqual(file2_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data3, test_device_instance_list)
        file3_after_test = test_monitor.folder.find_file_by_dab_id(test_file3.get_dab_id())
        self.assertEqual(file3_after_test.get_status(), expected_result)




