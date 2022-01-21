'''
project: slimmer maken multiconnectivity modem
author: Frank Montenij
Description: An enum class to represent the different categories the system supports.
'''

import enum

class Category(enum.Enum):
    """A Enum to specify the different stages the confirmation can be in"""
    WEATHER = "weather"
    LOCATION = "location"
    OTHER = "other"
    CAP = "CAP"