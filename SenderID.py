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

    def store_ID(self):
        with open(self.filename, 'a') as file:
            if os.stat(self.filename).st_size == 0:
                file.write(str(self.generate_ID()))

    def read_ID(self):
        with open(self.filename, mode='r', encoding='utf-8') as file:
            return uuid.UUID(file.readline())
