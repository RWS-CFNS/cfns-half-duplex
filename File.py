#!/usr/bin/python

class File:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.dab_id = 0
        self.message_type = 0

    def set_lines(self, path):
        my_lines = []  # Declare an empty list named mylines.
        with open(str(path+self.filename), 'rt') as my_file:  # Open lorem.txt for reading text data.
            for my_line in my_file:  # For each line, stored as myline,
                my_lines.append(my_line)  # add its contents to mylines.
        self.lines = my_lines
        self.dab_id = int(self.lines[0])
        self.message_type = int(self.lines[1])

    def get_dab_id(self):
        return self.dab_id

    def get_message_type(self):
        return self.message_type

    def get_coordinates(self):
        return float(self.lines[2]), float(self.lines[3])

    def get_lines(self):
        return self.lines

