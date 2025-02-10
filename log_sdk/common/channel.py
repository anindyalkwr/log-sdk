from enum import Enum


class Channel(Enum):
    """
    Enum representing the source of the log.
    """
    SENSOR = "Sensor"
    SYSTEM = "System"
    MANUAL_INPUT = "Manual Input"


    def __str__(self):
        return self.value
