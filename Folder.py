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

from File import File
import threading

class Folder:
    def __init__(self, path):
        self.lock = threading.Lock()
        self.path = path
        self.files = []

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path

    def get_list_files(self):
        return self.files

    def find_file_by_dab_id(self, dab_id):
        for file in self.files:
            if file.dab_id == dab_id:
                return file
            else:
                continue
        return False

    """
        Pass along a field and a value to find and return the first file that matches those values.
    """
    def find_files_by_field(self, field, value):
        found_files = []

        # If True field is not an attribute of File, so return False
        if not field in vars(File("")).keys():
            return False

        for file in self.files:
            with self.lock:
                attributes = vars(file)

            if attributes[field] == value:
                found_files.append(file)
            else:
                continue
        
        return found_files

    """
        This method takes in keyword arguments and a dab_id. The dab_id is used to find the file this method has to update.
        The kwargs are used to specify wich fields need to be changed to a different value.
    """
    def update_file(self, dab_id, **kwargs):
        file = self.find_file_by_dab_id(dab_id)

        if not file:
            print("File not found")
            return 

        for field_in_file, value in kwargs.items():
            if field_in_file == "status":
                file.set_status(value)
            elif field_in_file == "valid":
                file.set_valid(value)

        
    # def set_list_files(self):
    #     files = []
    #     for x in os.listdir(self.path):
    #         if x.endswith(".txt"):
    #             # Prints only text file present in My Folder
    #             files.append(x)
    #     self.files = files


# f1 = Folder('./correct/')
# # rl = f1.readlines()
# # dabid = f1.check_dab_id(rl)
# f1.get_list_files()
# f1.get_list_files()

