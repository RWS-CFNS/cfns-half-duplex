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

class Folder:
    def __init__(self, path):
        self.path = path
        self.files = []

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path

    def get_list_files(self):
        return self.files

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

