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

from Status import Status

class File:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.dab_id = 0
        self.message_type = 0
        self.status = Status.UNCONFIRMED 
        self.valid = True

    def set_lines(self, path):
        my_lines = []  # Declare an empty list named mylines.
        with open(str(path+self.filename), 'rt') as my_file:  # Open lorem.txt for reading text data.
            for my_line in my_file:  # For each line, stored as myline,
                my_lines.append(my_line)  # add its contents to mylines.
        self.lines = my_lines
        self.dab_id = int(self.lines[0])
        self.message_type = int(self.lines[1])

    def set_status(self, status):
        if type(status) == type(self.status):
            self.status = status

    def set_valid(self, valid):
        self.valid = valid

    def get_dab_id(self):
        return self.dab_id

    def get_message_type(self):
        return self.message_type

    def get_coordinates(self):
        return float(self.lines[2]), float(self.lines[3])

    def get_lines(self):
        return self.lines

    def get_status(self):
        return self.status

    def get_valid(self):
        return self.valid

