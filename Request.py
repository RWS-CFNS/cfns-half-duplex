import json
from abc import ABC, abstractmethod
from Folder import Folder

class Request(ABC):
    def __init__(self, folder: Folder):
        self.folder = folder

    @abstractmethod
    def parse(self):
        """A method to parse a request"""

    def build_information_dict(self, files):
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

        files = self.folder.find_files_by_field('sent_to_onboard_systems', False)
        
        return self.build_information_dict(files)


class CategoryRequest(Request):
    def __init__(self, folder, category):
        super().__init__(folder)
        self.category = category

    def parse(self):
        """A request to get the information from the files that belong to category"""

        files = self.folder.find_files_by_field('category', self.category)
        
        return self.build_information_dict(files)
    
    def build_response(self, information):
        """A method to build a response for a CategoryRequest"""
        return json.dumps({"reply": True, "category": self.category, "information": information})
        
class TestRequest(Request):
    def __init__(self, folder):
        super().__init__(folder)

    def parse(self):
        """To test the expandibility of the interface."""

