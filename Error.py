import enum

class Error(enum.Enum):
    NO_DICT = "Request is not a dict."
    INCORRECT_JSON_DECODER = "Request was not properly send with json."
    UNKOWN_REQUEST_TYPE = "Unkown request type."
    INCORRECT_FIELD = "The request does not contain all the required keys.\nSee the documentation for the required keys."


