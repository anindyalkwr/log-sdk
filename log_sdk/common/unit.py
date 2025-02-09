from enum import Enum


class UnitOfMeasurement(Enum):
    """
    Enum representing units of measurement for different sensor types.
    """
    HERTZ = "Hz"
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    BAR = "Bar"
    PASCAL = "Pa"
    LITERS_PER_SECOND = "L/s"
    AMPERE = "A"
    VOLTAGE = "V"
    PERCENT = "%"
    METERS_PER_SECOND = "m/s"
    NEWTON_METER = "Nm"
    LUX = "lux"
    PH_VALUE = "pH"


    def __str__(self):
        return self.value
    