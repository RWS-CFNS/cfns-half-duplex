import enum

class Status(enum.Enum):
    """A Enum to specify the different stages the confirmation can be in"""
    UNCONFIRMED = 1
    CONFIRMING = 2
    CONFIRMED = 3
    SKIP = 4
    