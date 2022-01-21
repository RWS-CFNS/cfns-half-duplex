'''
project: slimmer maken multiconnectivity modem
author: Frank Montenij
Description: A class that can generate an id which the system on land uses to seperate the different messages sent from the different ships.
             This class does not only generate the ID, but also is responsible for retrieving the id from a file and storing it to a file.
            
Changelog: Frank created the file.
'''

import uuid
import os

"""
    A Class to generate, store and retrieve an SenderID. This way even if the program shuts down or crashes
    the SenderID stays the same
"""
class SenderID:
    def __init__(self):
        self.filename = "id.txt"

    def generate_ID(self):
        return uuid.uuid4()

    """
        Store a new ID when the file is empty otherwise do nothing
    """
    def store_ID(self):   
        with open(self.filename, 'a') as file:
            if os.stat(self.filename).st_size == 0:
                file.write(str(self.generate_ID()))

    def read_ID(self):
        with open(self.filename, mode='r', encoding='utf-8') as file:
            return str(uuid.UUID(file.readline()))
