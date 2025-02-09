from enum import Enum


class Action(Enum):
    """
    Enum representing actions performed on a machine.
    """
    START = "Start"
    STOP = "Stop"
    MAINTENANCE = "Maintenance"
    ERROR_DETECTED = "Error Detected"
    RESET = "Reset"
    CALIBRATION = "Calibration"


    def __str__(self):
        return self.value
    
