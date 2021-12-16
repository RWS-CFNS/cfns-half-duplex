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

import time
import os
from Status import Status
from Category import Category

class File:
    def __init__(self, filename, status=Status.CONFIRMING, category=Category.OTHER):
        self.filename = filename
        self.lines = []
        self.dab_id = 0
        self.message_type = 0
        self.category = category
        self.coordinates = ()
        self.status = status
        self.valid = True
        self.sent_to_onboard_systems = False
        self.time_of_arrival = time.time()

    def set_lines(self, path):
        with open(str(path+self.filename), 'rt') as my_file: 
            for my_line in my_file: 
                # add the line to lines without the lineseperator in the string. Works for all operating systems
                self.lines.append(my_line.strip(os.linesep))

    """
        This method will extract the data from the lines and put it in the corresponding field.
    """
    def set_information(self):
        self.dab_id = int(self.lines[0])
        self.message_type = int(self.lines[1])
        self.category = Category(self.lines[2]) 

        if len(self.lines) > 3:  
            self.coordinates = (float(self.lines[3]), float(self.lines[4]))

    def set_status(self, status):
        if type(status) == type(self.status):
            self.status = status

    def set_valid(self, valid):
        self.valid = valid

    def set_sent_to_onboard_systems(self, sent):
        self.sent_to_onboard_systems = sent

    def get_lines(self):
        return self.lines

    def get_dab_id(self):
        return self.dab_id

    def get_message_type(self):
        return self.message_type

    def get_category(self):
        return self.category

    def get_coordinates(self):
        return self.coordinates 

    def get_status(self):
        return self.status

    def get_valid(self):
        return self.valid
    
    def get_sent_to_onboard_systems(self):
        return self.sent_to_onboard_systems

    def get_time_of_arrival(self):
        return self.time_of_arrival

