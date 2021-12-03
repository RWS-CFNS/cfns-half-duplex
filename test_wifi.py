from File import File
from Folder import Folder
from Status import Status
from main import Monitor, attach_devices
import unittest
import time

class WifiConfirmTester(unittest.TestCase):
    def test_updating_file(self):
        """Testcase to test if Folder can update fields in a File"""

        # Prepare the test
        test_folder = Folder("./correct")
        test_file = File("test")
        test_folder.files = [test_file]

        # Test if a folder can update the valid field in a file 
        expected_result = False
        test_folder.update_file(test_file.get_dab_id(), valid=False)    
        result = test_file.get_valid()
        self.assertEqual(result, expected_result)

        # Test if a folder can update the status field in a file 
        expected_result = Status.CONFIRMED
        test_folder.update_file(test_file.get_dab_id(), status=Status.CONFIRMED)    
        result = test_file.get_status()
        self.assertEqual(result, expected_result)

    def test_acknowledge_wifi(self):
        """
            Testcase to test if the Half-Duplex system in the current state can confirm a message using Wifi
            devices.csv should only contain the column information on row 1 and the information for the FiPy device using Wifi on row 2. For this test.
        """
        
        # Prepare the monitor
        test_folder = Folder("./correct")
        test_monitor = Monitor(test_folder)
        test_monitor.devices = attach_devices("devices.csv") # Fills the list of devices with one device so choose device is not necessary
        test_device_list = test_monitor.devices

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

        test_monitor.acknowledge(data1, test_device_list)
        file1_after_test = test_monitor.folder.find_file_by_dab_id(test_file1.get_dab_id())
        self.assertEqual(file1_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data2, test_device_list)
        file2_after_test = test_monitor.folder.find_file_by_dab_id(test_file2.get_dab_id())
        self.assertEqual(file2_after_test.get_status(), expected_result)

        test_monitor.acknowledge(data3, test_device_list)
        file3_after_test = test_monitor.folder.find_file_by_dab_id(test_file3.get_dab_id())
        self.assertEqual(file3_after_test.get_status(), expected_result)
