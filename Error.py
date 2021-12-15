import enum

class Error(enum.Enum):
    NO_DICT = "Error message: Request is not a dict."
    INCORRECT_JSON_DECODER = "Error message: Request was not properly send with json."
    UNKOWN_REQUEST_TYPE = "Error message: Unkown request type."
    INCORRECT_FIELD = "Error message: "


