import unittest
from Folder import Folder
import main
from Devices.Strategy import AISStrategy, EthernetStrategy, I2CStrategy

class ChoosingDevicesTester(unittest.TestCase):
    """A Class to test the part choosing the best device available."""

    def setUp(self):
        self.test_monitor = main.Monitor(Folder("test_path"))

    """
        This method is a help function for the tests: test_has_reach and test_failed_has_reach.
        It asks for all 5 the devices in test_devices1.csv if they have reach and stores it in results.
    """
    def has_reach_for_devices(self):
        results = []

        # Test has_reach of Wifi
        test_device = main.attach_devices("csv_test_files/test_devices1.csv")[0]
        result = test_device.has_reach()
        results.append(result)

        # Test has_reach of LoRa (FiPy)
        # test_device = main.attach_devices("csv_test_files/test_devices1.csv")[1]
        # result = test_device.has_reach()
        # results.append(result)

        # Test has_reach LoRa (on the Sodaq One)
        # test_device = main.attach_devices("csv_test_files/test_devices1.csv")[2]
        # test_device.set_technology("LoRa")
        # result = test_device.has_reach()
        # results.append(result)

        # Test has_reach of LTE
        test_device = main.attach_devices("csv_test_files/test_devices1.csv")[3]
        result = test_device.has_reach()
        results.append(result)

        # Test has_reach AIS
        test_device = main.attach_devices("csv_test_files/test_devices1.csv")[4]
        result = test_device.has_reach()
        results.append(result)

        return results

    """
        This test evaluates if the has reach works when all of the devices are within range.
    """
    def test_has_reach(self):
        results = self.has_reach_for_devices()
        AIS_result = results.pop(len(results) - 1)

        for result in results:
            self.assertEqual(result, True)
        self.assertEqual(AIS_result, None)

    """
        This test evaluates if the has reach works when none of the devices are within range.
    """
    def test_failed_has_reach(self):
        results = self.has_reach_for_devices()
        AIS_result = results.pop(len(results) - 1)

        for result in results:
            self.assertNotEqual(result, True)
        self.assertEqual(AIS_result, None)

    """
        This test evaluates if the filter based on has_reach works as intended.
        It is being tested by passing along the different inputs and checks if the output is as expected.
    """
    def test_filter_devices_on_reach(self):
        # "test_devices1.csv" contains a device that can not determine if they have reach.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices1.csv")
        expected_no_has_reach_device = self.test_monitor.devices[0]
        devices_have_reach, no_has_reach_devices= self.test_monitor.filter_devices_on_reach()
        result = no_has_reach_devices[0]
        self.assertEqual(devices_have_reach, [])
        self.assertEqual(result, expected_no_has_reach_device)

        # "test_devices2.csv" contains a device that can determine if they have reach. But are out of reach.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices2.csv")
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()
        self.assertEqual(devices_have_reach, [])
        self.assertEqual(no_has_reach_devices, [])

        # "test_devices3.csv" contains a device that can determine if they have reach. Moreover they have reach.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices3.csv")
        expected_device = self.test_monitor.devices[0]
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()
        result = devices_have_reach[0]
        self.assertEqual(result, expected_device)
        self.assertEqual(no_has_reach_devices, [])

    """
        This test test if the method choose_device is able to choose the best device for all the different inputs. 
    """
    def test_get_highest_priority_device(self):
        # Test if choose device can choose the device that has priority one.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices1.csv")
        devices_have_reach = self.test_monitor.devices

        # Take the first element because get_highest_priority_device returns a list because
        result_device = self.test_monitor.get_highest_priority_device(devices_have_reach) 
        self.assertTrue(isinstance(result_device.strategy, EthernetStrategy))
        self.assertEqual(result_device.technology, "Wifi")

        # Test if choose device can choose the highest priority device when the device with priority one is not present.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices2.csv")
        devices_have_reach = self.test_monitor.devices
        result_device = self.test_monitor.get_highest_priority_device(devices_have_reach=devices_have_reach, no_has_reach_devices=[])[0]
        self.assertTrue(isinstance(result_device.strategy, I2CStrategy))
        self.assertEqual(result_device.technology, "LoRa")

        # test if choose device can detect that there is no device available and returns False.
        with self.assertRaises(ValueError):
            self.test_monitor.get_highest_priority_device([])

    """
        This test is the system test and tests the new part from beginning to end for most of the available inputs. 
        The inputs with LoRa devices are not implemented in this version.
    """
    def test_choose_device(self):
        # Test if the system choosing devices works when the device with priority one is available.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices1.csv")
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()

        result_device = self.test_monitor.choose_device(devices_have_reach, no_has_reach_devices)[0]
        self.assertTrue(isinstance(result_device.strategy, EthernetStrategy))
        self.assertEqual(result_device.technology, "Wifi")

        # Test if the system choosing devices works when the device with priority one is not available. Is it capable of choosing the best from the rest.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices2.csv")
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()
 
        result_device = self.test_monitor.choose_device(devices_have_reach, no_has_reach_devices)[0]
        self.assertTrue(isinstance(result_device.strategy, EthernetStrategy))
        self.assertEqual(result_device.technology, "LTE")

        # Test if the system choosing devices works when only AIS is available. So a tech which cannot determine if it is within reach.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices3.csv")
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()

        result_device = self.test_monitor.choose_device(devices_have_reach, no_has_reach_devices)[0]
        self.assertTrue(isinstance(result_device.strategy, AISStrategy))
        self.assertEqual(result_device.technology, "AIS")

        # Test if the system choosing devices works when there are no devices available. It should return False.
        self.test_monitor.devices = []
        devices_have_reach, no_has_reach_devices = self.test_monitor.filter_devices_on_reach()

        result_device = self.test_monitor.choose_device(devices_have_reach, no_has_reach_devices)
        self.assertEqual(result_device, [])


