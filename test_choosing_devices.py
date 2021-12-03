import unittest
import main
from Devices.Strategy import AISStrategy, EthernetStrategy, I2CStrategy

class ChoosingDevicesTester(unittest.TestCase):
    def setUp(self):
        self.test_monitor = main.Monitor("folder")
    
    def has_reach_for_devices(self):
        test_device = main.attach_devices("csv_test_files/test_devices1.csv")[0]
        results = []

        # Test has_reach of Wifi
        test_device.set_technology("Wifi")
        result = test_device.has_reach()
        self.append(result)

        # Test has_reach of LoRa (on the FiPy)
        # test_device_fipy.set_technology("LoRa")
        # result = test_device_fipy.has_reach()
        # self.append(result)
        
        # Test has_reach of LTE
        test_device.set_technology("LTE")
        result = test_device.has_reach()
        self.append(result)

        # Test has_reach LoRa (on the Sodaq One)
        # test_device = test_monitor.attach_device("csv_test_files/test_devices1.csv")[1]
        # test_device.set_technology("LoRa")
        # result = test_device.has_reach()
        # self.append(result)

        return results

    def test_has_reach(self):
        results = self.has_reach_for_devices()

        for result in results:
            self.assertEqual(result, True)

    def test_failed_has_reach(self):
        results = self.has_reach_for_devices()

        for result in results:
            self.assertNotEqual(result, True)

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

    def test_no_devices_available(self):
        # Make sure devices is empty!
        self.assertEqual(self.test_monitor.devices, [])

        # Test if choose devices returns False when there are no devices available
        self.assertFalse(self.test_monitor.choose_device())

    def test_choose_device(self):
        # Test if choose device can choose the device that has priority one.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices1.csv")
        expected_device = self.test_monitor.devices[0]
        self.assertEqual(expected_device.strategy, EthernetStrategy)
        self.assertEqual(expected_device.technology, "Wifi")
        
        result_device = self.test_monitor.choose_device()[0]
        self.assertEqual(result_device.strategy, EthernetStrategy)
        self.assertEqual(result_device.technology, "Wifi")

        # Test if choose device can choose the highest priority device when the device with priority one is not present.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices2.csv")
        expected_device = self.test_monitor.devices[0]
        self.assertEqual(expected_device.strategy, I2CStrategy)
        self.assertEqual(expected_device.technology, "LoRa")
        
        result_device = self.test_monitor.choose_device()[0]
        self.assertEqual(result_device.strategy, I2CStrategy)
        self.assertEqual(result_device.technology, "LoRa")
        
        # Test if choose device can choose the device(s) that cannot determine if they are within reach.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices3.csv")
        expected_device = self.test_monitor.devices[0]
        self.assertEqual(expected_device.strategy, AISStrategy)
        self.assertEqual(expected_device.technology, "AIS")
        
        result_device = self.test_monitor.choose_device()[0]
        self.assertEqual(result_device.strategy, AISStrategy)
        self.assertEqual(result_device.technology, "AIS")

        # test if choose device can detect that there is no device available and returns False.
        self.test_monitor.devices = main.attach_devices("csv_test_files/test_devices4.csv")
        expected_result = False
        result = self.test_monitor.choose_device()
        self.assertEqual(result, expected_result)