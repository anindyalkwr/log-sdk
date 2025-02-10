from enum import Enum


class SensorType(Enum):
    """
    Enum representing different types of sensors in industrial manufacturing.
    """
    VIBRATION = "Vibration Sensor"
    TEMPERATURE = "Temperature Sensor"
    PRESSURE = "Pressure Sensor"
    HUMIDITY = "Humidity Sensor"
    FLOW = "Flow Sensor"
    ELECTRICAL = "Electrical Sensor"
    CURRENT = "Current Sensor"
    GAS = "Gas Sensor"
    SPEED = "Speed Sensor"
    TORQUE = "Torque Sensor"
    LIGHT = "Light Sensor"
    PH = "pH Sensor"


    def __str__(self):
        return self.value
    