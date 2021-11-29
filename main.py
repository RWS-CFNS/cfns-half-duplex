import os
import sys
import argparse
import csv
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from Devices.Device import Device
from Devices.Strategy import AISStrategy, EthernetStrategy, I2CStrategy, SPIStrategy
from Interface.Ethernet import Ethernet
from Interface.I2C import I2C
from Interface.SPI import SPI
from Interface.UART import UART
from Folder import Folder
from File import File
from Status import Status
from SenderID import SenderID

class Monitor(PatternMatchingEventHandler):
    """A Class to handle incoming DAB files."""

    def __init__(self, folder):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], ignore_directories=True, case_sensitive=False)
        self.folder = folder
        self.devices = []
        self.devices_csv_filename = ""

    """
        This method creates the confirmation dictionary
    """
    def create_confirmation_dict(self, dab_id, message_type, time_of_arrival):
        senderID = SenderID()

        # Stores an id when the file with the id is empty.
        senderID.store_ID()
        
        confirmation_dict = {
            "dab_id": dab_id,
            "message_type": message_type,
            "dab_msg_arrived_at": time_of_arrival,
            "sender": senderID.read_ID() # Read the id from id.txt
        }

        if message_type == 4:
            confirmation_dict["dab_signal"] = get_dab_signal()

        return confirmation_dict

    """
        This method will be called when the observer detects a file being created in the folder that it observes.
    """
    def on_created(self, event):
        print(event.src_path, event.event_type)

        # Save new DAB+ message as File object and fill it with the data from the .txt file.
        new_file = File(str(event.src_path).replace(self.folder.path, ""))
        new_file.set_lines(self.folder.path)
        new_file.set_information()

        # Get DAB+ ID ,Message Type and time_of_arrival
        dab_id = new_file.get_dab_id()
        message_type = new_file.get_message_type()
        time_of_arrival = new_file.get_time_of_arrival()

        """
            Check if File is already in folder and confirmed, if so abort the confirmation and do not store the file.
            If the File is not in the folder store the new_file in the folder. 
            Else do not append the file and continue confirming the file.
        """
        file_in_folder = self.folder.find_file_by_dab_id(dab_id)
        if file_in_folder and file_in_folder.status == Status.CONFIRMED:
            return
        elif not file_in_folder:
            # Add new DAB+ message to the Folder object
            self.folder.files.append(new_file)

        # Show the contents of the file
        for line in new_file.get_lines():
            print(f'line: {line}')

        # Build the confirmation dict which contains all the necessary information to acknowledge a DAB messsage
        data = self.create_confirmation_dict(dab_id, message_type, time_of_arrival)
        
        # Choose the best possible device or devices if the reach of the device can not be determined
        self.devices = attach_devices(self.devices_csv_filename)
        devices = self.choose_device()

        # If there is no device available. Abort the acknowledgment
        if not devices:
            self.folder.update_file(dab_id, status=Status.SKIP)
            return
        else:           
            # Start the acknowledgment
            self.acknowledge(data, devices)

    """
        This method chooses the best device based on the reach the technology of the device has, the specifics of the used technology and the availability of the device. 
        To choose the device that fits best for the current situation
    """
    def choose_device(self):
        # Check if devices is empty 
        if not self.devices:
            return False

        # Initialize the lists to fill with the correct devices
        devices_have_reach = []
        devices_not_able_to_calc_reach = []

        # Fill the lists with the correct devices
        for device in self.devices: 
            has_reach = device.has_reach()
            if has_reach:
                devices_have_reach.append(device)  
            elif has_reach == None:
                devices_not_able_to_calc_reach.append(device)

        if devices_have_reach:
            # Find the device with the highest priority. Highest priority is the lowest device.priority value
            return [min(devices_have_reach, key= lambda device: device.priority)]
        elif devices_not_able_to_calc_reach:
            # Choose all the possible devices
            return devices_not_able_to_calc_reach
        else: 
            # If there is no device within reach or no device in devices_not_able_to_calc_reach. return False
            return False

    """
        This method is responsible for acknowledging the DAB file with all the available devices.
    """
    def acknowledge(self, data, devices):
        for device in devices:
            # Change data when using the Sodaq One. Otherwise add the technology used by the device.
            if isinstance(device.strategy, I2CStrategy):
                data = {key:value for key, value in data.items() if key == "dab_id" or key == "message_type"}
            else:
                data["technology"] = device.get_technology()

            # Get the result of the acknowledgment
            reply = device.acknowledge(data)

            if not reply:
                # Update the file to SKIP, because the acknowledgment failed for an unkown reason
                self.folder.update_file(data.get("dab_id"), status=Status.SKIP)
                return

            if isinstance(device.strategy, EthernetStrategy):
                # The new status will be CONFIRMATION_SENT if the dab_id match and the technology is not Wifi. If the dab_id does not match the status will be SKIP.
                new_status = Status.CONFIRMATION_SENT if data.get("dab_id") == reply["ack_information"][0] else Status.SKIP

                if device.get_technology() == "Wifi":
                    # Change the status to confirmed if the tech happens to be Wifi. Only for this technology you can be certain that the message was confirmed or not.
                    new_status = Status.CONFIRMED if data.get("dab_id") == reply["ack_information"][0] else Status.SKIP
                    
                    # Update the status and validity of the files that have been received by the server.
                    for entry in reply.get("different_ack_information"):
                        self.folder.update_file(entry[0], status=Status.CONFIRMED, valid=entry[1])

                # Update the status of the file that this confirmation tries to confirm to new_status. Which is CONFIRMATION_SENT when the technology is not Wifi otherwise it will be CONFIRMED.
                self.folder.update_file(data.get("dab_id"), status=new_status, valid=reply["ack_information"][1])
            else:
                # implements the change status to skip or confirmed when the device used the i2c strategy.
                new_status = Status.CONFIRMATION_SENT if reply else Status.SKIP
                self.folder.update_file(data.get("dab_id"), status=new_status)

            # print the status for every file
            print("\nStatus of files (dab_id, file status")
            for file in self.folder.files:
                print(file.get_dab_id(), file.get_status())

    def retry_failed_confirmation(self):
        for file in self.folder.files:
            if file.get_status() == Status.UNCONFIRMED:
                # Build the confirmation dict which contains all the necessary information to acknowledge a DAB messsage
                data = self.create_confirmation_dict(file.get_dab_id(), file.get_message_type(), file.get_time_of_arrival())
                
                # Choose the best possible device or devices if the reach of the device can not be determined
                self.devices = attach_devices(self.devices_csv_filename)
                devices = self.choose_device()

                thread = threading.Thread(target=self.acknowledge, args=(data, devices))
                thread.start()
            elif file.get_status() == Status.SKIP:
                file.set_status(Status.UNCONFIRMED)

"""
    This function is the main function that handles starting the monitor and observer
"""
def execute():
    # create parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument("devices")
    parser.add_argument("folder")

    # parse the arguments
    args = parser.parse_args()

    # Create Folder object with path of folder
    dab_folder = Folder(os.path.expanduser(args.folder))

    # Assign folder to be monitored
    event_handler = Monitor(dab_folder)
    observer = Observer()
    observer.schedule(event_handler, path=event_handler.folder.path, recursive=True)

    # Let the monitor no what the filename of devices is. So it can attach_devices later.
    event_handler.devices_csv_filename = args.devices

    # Start the observing of the folder args.folder. When something changes start on_created in the event_handler
    observer.start()
    print("Monitoring started")
    try:
        while True:
            event_handler.retry_failed_confirmation()
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring Stopped")
    observer.join()

def get_dab_signal():
    return 20

"""
    This function reads all the device information from a csv file. Then converts that infromation to a Device object. 
    And adds the object to the attribute devices belonging to Monitor.
"""
def attach_devices(csv_parameter):
    listed_devices = []

    try:
        with open(csv_parameter, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                    
                device = Device(row["name"], row["branch"], row["model"], row["technology"], int(row["priority"]))
                if int(row["interface_type"]) == 0:
                    print(row["name"])
                    interface = UART()
                    interface.init_serial(row["address"], int(row["setting"]))
                    strategy = AISStrategy(interface)
                    listed_devices.append(device)

                if int(row["interface_type"]) == 1:
                    print(row["name"])
                    interface = I2C()
                    interface.init_i2c(int(row["address"]))
                    strategy = I2CStrategy(interface)
                    listed_devices.append(device)

                if int(row["interface_type"]) == 2:
                    print(row["name"])
                    interface = Ethernet()
                    interface.init_socket(row["address"], int(row["setting"])) # Address and setting are here the ip_address and the portnumber of the target device.
                    strategy = EthernetStrategy(interface)
                    listed_devices.append(device)

                if int(row["interface_type"]) == 3:
                    print(row["name"])
                    interface = SPI()
                    interface.init_spi(int(row["address"]), int(row["setting"]))
                    strategy = SPIStrategy(interface)
                    listed_devices.append(device)
                
                device.set_strategy(strategy)
               
                line_count += 1
            print(f'Processed {line_count} lines.')

        if line_count > 1:
            return listed_devices
        else:
            print(f"No devices are listed. Configure {csv_parameter} and execute the program again")
            sys.exit()
    except RuntimeError:
        print("Could not open list with devices")


if __name__ == "__main__":
    try:
        execute()
    except RuntimeError:
        print("Could not execute programm")