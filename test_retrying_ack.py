import time
import unittest
from Folder import Folder
from File import File
from Status import Status
import main

class RetryingAckTester(unittest.TestCase):
    def setUp(self):
        self.test_monitor = main.Monitor(Folder("test_path"))
        status = Status.UNCONFIRMED

        # Fill the folder with files with each of them having a different status
        for number in range(1, len(Status) + 1):
            # Create the File itself and change the attributes to distinguish the files from each other.
            file_to_add = File(f"test{number}")
            file_to_add.dab_id = number
            file_to_add.message_type = 1
            
            # Set the status of the file, so every status is tested.
            file_to_add.set_status(status)
            status = status.nextStatus()

            # Finally add the file to the monitor
            self.test_monitor.folder.files.append(file_to_add)

    def test_retrying_ack(self):
        self.test_monitor.devices_csv_filename = "csv_test_files/test_devices1.csv"
        self.test_monitor.retry_failed_confirmation()

        for file in self.test_monitor.folder.files:
            if file.dab_id == 1:
                # Based on the time it takes to confirm a message with wifi
                time.sleep(3)
                
                self.assertEqual(file.get_status(), Status.CONFIRMED)
            elif file.dab_id in [2, 3, 5]:
                self.assertEqual(file.get_status, Status(file.dab_id))
            elif file.dab_id == 4:
                self.assertEqual(file.get_status(), Status.UNCONFIRMED)
            else:
                raise NotImplementedError(f"There is not test defined for a file with dab_id: {file.dab_id}")


        
        



