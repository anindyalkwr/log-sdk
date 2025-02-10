from enum import Enum


class Action(Enum):
    """
    Enum representing actions performed on a machine.
    """
    START = "Start"
    STOP = "Stop"
    MAINTENANCE = "Maintenance"
    CALIBRATION = "Calibration"


    def __str__(self):
        return self.value
