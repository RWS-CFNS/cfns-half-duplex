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

import main
from File import File
from Folder import Folder
from Device import Device
from Interface import Interface
from main import Monitor, attach_devices

from Status import Status

''''
project: Half-Duplex
author: Alfred Espinosa Encarnación, Frank Montenij
date: 30-03-2021, 11-11-2021

Description: Testing method to test the functionalities of Half-Duplex. The class MyTestCase has been written by Alfred. Frank Wrote the class WifiConfirmTester
'''

class MyTestCase(unittest.TestCase):
    def test_file(self):

        # expected values when reading from dab+ message "bb.txt"
        assess_dab_id = 67
        assess_message_type = 4
        assess_latitude = 52.6525
        assess_longitude = 4.7448

        # read the data from dab+ message
        test_filename = "bb.txt"
        test_path = "correct/"
        test_file = File(test_filename)
        test_file.set_lines(test_path)

        # assign data from dab+ message to variables
        test_dab_id = test_file.get_dab_id()
        test_message_type = test_file.get_message_type()
        test_latitude, test_longitude = test_file.get_coordinates()

        # check if the data from dab+ message equals to the expected data
        self.assertEqual(assess_dab_id, test_dab_id)
        self.assertEqual(assess_message_type, test_message_type)
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
        test_device = Device("AIS Transponder1", "True Heading", "AIS Base Station", 0)
        result_name = test_device.get_name()
        result_branch = test_device.get_branch()
        result_model = test_device.get_model()
        result_interface = test_device.get_interface()

        self.assertEqual("AIS Transponder1", result_name)
        self.assertEqual("True Heading", result_branch)
        self.assertEqual("AIS Base Station", result_model)
        self.assertEqual(0, result_interface)

        test_device.set_name("test_name")
        test_device.set_branch("python_unit")
        test_device.set_model("PU-00")
        test_device.set_interface(1)

        new_result_name = test_device.get_name()
        new_result_branch = test_device.get_branch()
        new_result_model = test_device.get_model()
        new_result_interface = test_device.get_interface()

        self.assertEqual("test_name", new_result_name)
        self.assertEqual("python_unit", new_result_branch)
        self.assertEqual("PU-00", new_result_model)
        self.assertEqual(1, new_result_interface)

    def test_interface(self):
        test_interface = Interface.Interface(0)
        self.assertEqual(0, test_interface.interface_type)
        test_interface.get_rs232_settings()
        with self.assertRaises(AttributeError):
            test_interface.get_ethernet_settings()

    def test_rs232(self):
        test_rs232 = Interface.UART()
        #test_rs232.init_serial("/dev/ttyUSB0", 115200)
        test_rs232.set_port("/dev/ttyUSB0")
        test_rs232.set_baudrate(38400)
        result_port = test_rs232.get_port()
        result_baudrate = test_rs232.get_baudrate()

        self.assertEqual("/dev/ttyUSB0", result_port)
        self.assertEqual(38400, result_baudrate)

        self.assertEqual(False, test_rs232.close_rs232())

    def test_i2c(self):
        test_i2c = Interface.I2C()
        #test_i2c.init_i2c(4)
        test_i2c.set_address(4)
        self.assertEqual(4, test_i2c.get_address())

    def test_ethernet(self):
        test_ethernet = Interface.Ethernet()
        test_ethernet.init_socket("192.168.0.101", 1234)

        self.assertEqual("192.168.0.101", test_ethernet.get_ip_address())
        self.assertEqual(1234, test_ethernet.get_port())
        test_ethernet.close_socket()


    def test_spi(self):
        test_spi = Interface.SPI()
        #test_spi.init_spi(0, 1)
        test_spi.set_spi_bus(0)
        test_spi.set_spi_device(1)

        self.assertEqual(0, test_spi.get_spi_bus())
        self.assertEqual(1, test_spi.get_spi_device())

    def test_acknowledge(self):
        test_monitor = Monitor("./correct")
        main.attach_devices("devices.csv")
        #test_monitor.acknowledge(67, 1)

class WifiConfirmTester(unittest.TestCase):
    def test_updating_file(self):
        """Testcase to test if Folder can update fields in a File"""

        # Prepare the test
        test_folder = Folder("./correct")
        test_file = File("test")
        test_folder.files[test_file]

        # Test if a folder can update the valid field in a file 
        expected_result = False
        test_folder.update_confirmed_in_file(test_file.get_dab_id(), valid=False)    
        result = test_file.get_valid()
        self.assertEqual(result, expected_result)

        # Test if a folder can update the status field in a file 
        expected_result = Status.CONFIRMED
        test_folder.update_confirmed_in_file(test_file.get_dab_id(), status=Status.CONFIRMED)    
        result = test_file.get_status()
        self.assertEqual(result, expected_result)

    def test_acknowledge_wifi(self):
        """Testcase to test if the Half-Duplex system in the current state can confirm a message using Wifi"""
        
        # Prepare the monitor
        test_folder = Folder("./correct")
        test_monitor = Monitor(test_folder)
        test_monitor.devices = attach_devices() 

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
        test_monitor.folder.files[test_file1, test_file2, test_file3]

        # Create the data to send
        time_of_arrival = time.time()
        data1 = test_monitor.create_confirmation_dict(test_file1.get_dab_id(), test_file1.get_message_type(), time_of_arrival)
        data2 = test_monitor.create_confirmation_dict(test_file2.get_dab_id(), test_file2.get_message_type(), time_of_arrival)
        data3 = test_monitor.create_confirmation_dict(test_file3.get_dab_id(), test_file3.get_message_type(), time_of_arrival)

        # Here the tests will be executed and determined if they were a succes or not
        expected_result = Status.CONFIRMED

        test_monitor.acknowledge(data1)
        file1_after_test = test_monitor.folder.find_file_by_dab_id(test_file1.get_dab_id())
        self.assertEqual(file1_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data2)
        file2_after_test = test_monitor.folder.find_file_by_dab_id(test_file2.get_dab_id())
        self.assertEqual(file2_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data3)
        file3_after_test = test_monitor.folder.find_file_by_dab_id(test_file3.get_dab_id())
        self.assertEqual(file3_after_test.get_status(), expected_result)

def main():
    tester = WifiConfirmTester()

    test_name = input("Welke test wilt u uitvoeren? ")
    test_suite = get_test_suite(test_name, tester)

    unittest.TextTestRunner().run(test_suite)

"""
    This function loops through all the attributes of get_function_names_startwith_test if the attribute is a function of _class append the function_name to function_names.
    After that filter the function names that start with "test". now you have a list of the function names that start with "test" and belong to _class.
"""
def get_function_names_startwith_test(_class):
    import types

    functionNames = []
    for entry, value in _class.__class__.__dict__.items():
        if (isinstance(value, types.FunctionType)):
            functionNames.append(entry)
    
    return [function_name for function_name in functionNames if function_name.startswith("test")]

def get_test_suite(test_name, tester_class):
    function_names = get_function_names_startwith_test(tester_class)

    suite = unittest.TestSuite()
    print(function_names)
    print(test_name)
    if test_name in function_names:
        suite.addTest(tester_class.__class__(test_name))
    else:
        print("test_name not a test function in the test_class")

    return suite

if __name__ == '__main__':
    main()
