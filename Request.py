import json
from abc import ABC, abstractmethod

from Category import Category

class Request(ABC):
    def __init__(self, folder):
        self.folder = folder

    @abstractmethod
    def parse(self):
        """A method to parse a request"""

    """
        Get all the files for wich the field has the value value and is valid
    """
    def get_files(self, field, value, valid=True):
        files = self.folder.find_files_by_field(field, value)
        files = [file for file in files if file.get_valid() == valid]

        return files

    def build_information_list(self, files):
        information = []
        for file in files:
            information.append((file.get_dab_id(), file.get_lines()[1:]))

        return information

    def build_response(self, information):
        """A general method to build a response"""

        return json.dumps({"reply": True, "information": information})

class LatestRequest(Request):
    def __init__(self, folder):
        super().__init__(folder)

    def parse(self):
        """A request to get the latest unsent valid information."""     

        files = self.get_files('sent_to_onboard_systems', False)

        return self.build_information_list(files)

class CategoryRequest(Request):
    def __init__(self, folder, category):
        super().__init__(folder)
        self.category = Category(category)

    def parse(self):
        """A request to get the information from the files that belong to category"""

        files = self.get_files('category', self.category)
        
        return self.build_information_list(files)
    
    def build_response(self, information):
        """A method to build a response for a CategoryRequest"""
        return json.dumps({"reply": True, "category": self.category, "information": information})

class TestRequest(Request):
    def __init__(self, folder):
        super().__init__(folder)

    def build_information_list(self):
        return [(1, 4, "other", (1.1234, 5,6789))]

    def parse(self):
        """To test the expandibility of the interface."""

        return self.build_information_list()