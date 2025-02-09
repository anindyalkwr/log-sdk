from enum import Enum


class DataCenter(Enum):
    """
    Enum representing different locations where machines are installed.
    """
    FACTORY_1 = "Factory 1"
    FACTORY_2 = "Factory 2"
    WAREHOUSE = "Warehouse"
    POWER_PLANT = "Power Plant"
    CHEMICAL_PLANT = "Chemical Plant"
    OIL_REFINERY = "Oil Refinery"


    def __str__(self):
        return self.value
    