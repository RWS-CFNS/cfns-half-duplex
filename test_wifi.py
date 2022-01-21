'''
project: slimmer maken multiconnectivity modem
author: Frank Montenij
Description: A testcase to test the acknwoledging of DAB messages using WiFi.

Changelog: Frank created the file.
'''

from File import File
from Folder import Folder
from Status import Status
import unittest


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
