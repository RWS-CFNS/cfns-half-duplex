import os
import sys
import argparse
import csv
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from Devices.Device import Device
from Folder import Folder
from File import File
from Status import Status
from SenderID import SenderID
import time

class Monitor(PatternMatchingEventHandler):
    """A Class to handle incoming DAB files."""

    def __init__(self, folder):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], ignore_directories=True, case_sensitive=False)
        self.folder = folder
        self.devices = []

    """
        This method creates the confirmation dictionary
    """
    def create_confirmation_dict(self, dab_id, message_type, time_of_arrival):
        SenderID().store_ID()
        
        return {
            "dab_id": dab_id,
            "message_type": message_type,
            "dab_msg_arrived_at": time_of_arrival,
            "sender": SenderID().read_ID()
        }

    """
        This method will be called when the observer detects a file being created in the folder that it observes.
    """
    def on_created(self, event):
        # This var keeps track of the time of arrival of a dab message
        time_of_arrival = time.time()

        print(event.src_path, event.event_type)
        time.sleep(1)

        # Save new DAB+ message as File object
        new_file = File(str(event.src_path).replace(self.folder.path, ""))

        # Add new DAB+ message to the Folder object
        self.folder.files.append(new_file)
        new_file.set_lines(self.folder.path)

        # Get DAB+ ID & Message Type
        dab_id = new_file.get_dab_id()
        message_type = new_file.get_message_type()

        # Show the contents of the file
        for line in new_file.get_lines():
            print(f'line: {line}')

        # Build the confirmation dict which contains all the necessary information to acknowledge a DAB messsage
        data = self.create_confirmation_dict(dab_id, message_type, time_of_arrival)
        if message_type == 4:
            data["dab_signal"] = get_dab_signal()
        
        # Choose the best possible device or devices if the reach of the device can not be determined
        devices = self.choose_device()

        # If there is no device available abort the acknowledgment
        if not devices:
            self.folder.update_file(dab_id, status=Status.SKIP)
            return

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

        # This are the devices that are in reach of a receiver that can receive data using their technology
        devices_have_reach = [device for device in self.devices.copy() if device.has_reach()]

        # This are the devices that can not determine if they are within reach or not
        devices_not_able_to_calc_reach = [device for device in self.devices.copy() if device.has_reach() is None]

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
            # Add the technology to the confirmation dict
            data["technology"] = device.get_technology()
            reply = device.acknowledge(data)

            if not reply:
                # Update the file to SKIP, because the acknowledgment failed for an unkown reason
                self.folder.update_file(data.get("dab_id"), status=Status.SKIP)
                return

            if device.get_technology() is "Wifi":
                print("TESTING")
                # Change the status to confirmed if the dab_id match otherwise change the data["dab_id"] to Status.SKIP
                new_status = Status.CONFIRMED if data.get("dab_id") == reply["ack_information"][0] else Status.SKIP
                self.folder.update_file(data.get("dab_id"), status=new_status, valid=reply["ack_information"][1])

                for entry in reply.get("AIS_ack_information"):
                    self.folder.update_file(entry[0], status=Status.CONFIRMED, valid=entry[1])

                for entry in reply.get("invalid_dab_confirmations"):
                    self.folder.update_file(entry[0], valid=entry[1])

                # print the status for every file
                for file in self.folder.files:
                    print(file.get_status())
            elif device.get_technology() is "LoRaWAN":
                # TODO
                ...
            elif device.get_technology() is "LTE":
                # TODO
                ...
            else:
                # TODO wat als het AIS, VDES...
                ...        

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

    # Assign list of devices attached to the system
    event_handler.devices = attach_devices(args.devices)

    # Start the observing of the folder args.folder. When something changes start on_created in the event_handler
    observer.start()
    print("Monitoring started")
    try:
        while (True):
            time.sleep(1)

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
                    
                device = Device(row["name"], row["branch"], row["model"], int(row["interface_type"]), row["technology"], int(row["priority"]))
                if int(row["interface_type"]) == 0:
                    print(row["name"])
                    device.interface.init_serial(row["address"], int(row["setting"]))
                    listed_devices.append(device)

                if int(row["interface_type"]) == 1:
                    print(row["name"])
                    device.interface.init_i2c(int(row["address"]))
                    listed_devices.append(device)

                if int(row["interface_type"]) == 2:
                    print(row["name"])
                    device.interface.init_socket(row["address"], int(row["setting"]))
                    listed_devices.append(device)

                if int(row["interface_type"]) == 3:
                    print(row["name"])
                    device.interface.init_spi(int(row["address"]), int(row["setting"]))
                    listed_devices.append(device)
                    
                line_count += 1
            print(f'Processed {line_count} lines.')

        if line_count > 1:
            return listed_devices
        else:
            print("No devices are listed. Configure {} and execute the program again".format(csv_parameter))
            sys.exit()
    except RuntimeError:
        print("Could not open list with devices")


if __name__ == "__main__":

    try:
        execute()
    except RuntimeError:
        print("Could not execute programm")