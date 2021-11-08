import enum

class Status(enum.Enum):
    UNCONFIRMED = 1
    CONFIRMING = 2
    CONFIRMED = 3
    SKIP = 4
    