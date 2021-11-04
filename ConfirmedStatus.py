import enum

class ConfirmedStatus(enum.Enum):
    UNCOFIRMED = 1
    CONFIRMING = 2
    CONFIRMED = 3
    SKIP = 4
    