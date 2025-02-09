from enum import Enum


class Product(Enum):
    """
    Enum representing different machine types or products in the manufacturing industry.
    """
    MACHINE_MONITORING = "Machine Monitoring"
    FACTORY_AUTOMATION = "Factory Automation"
    POWER_PLANT = "Power Plant"
    OIL_AND_GAS = "Oil and Gas"
    CHEMICAL_PROCESSING = "Chemical Processing"
    HEAVY_EQUIPMENT = "Heavy Equipment"
    METAL_PRODUCTION = "Metal Production"


    def __str__(self):
        return self.value
    