import enum

class Status(enum.Enum):
    """A Enum to specify the different stages the confirmation can be in"""
    UNCONFIRMED = 1
    CONFIRMING = 2
    CONFIRMED = 3
    SKIP = 4
    CONFIRMATION_SENT = 5

    def next_status(self):
        next_status = self.value + 1 if self.value + 1 <= len(Status) else 1
        return Status(next_status)

    def previous_status(self):
        previous_status = self.value - 1 if self.value - 1 >= 1 else len(Status)
        return Status(previous_status)