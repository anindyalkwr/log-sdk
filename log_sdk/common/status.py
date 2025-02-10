from enum import Enum


class Status(Enum):
    """
    Enum representing machine or sensor status.
    """
    NORMAL = "Normal"
    WARNING = "Warning"
    CRITICAL = "Critical"
    FAULT = "Fault"


    def __str__(self):
        return self.value
    