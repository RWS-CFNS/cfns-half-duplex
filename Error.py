'''
project: slimmer maken multiconnectivity modem
author: Frank Montenij
Description: An enum class to represent the different categories the system supports.
'''

import enum

class Error(enum.Enum):
    NO_DICT = "Request is not a dict."
    INCORRECT_JSON_DECODER = "Request was not properly send with json."
    UNKOWN_REQUEST_TYPE = "Unkown request type."
    INCORRECT_FORMAT = "The request is not in the required format. See the documentation for correct format."


