from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class TemperatureLogData(BaseSensorLogData):
    """
    Logs temperature sensor data
    """

    def __init__(self, **kwargs):
        """
        Unit: Celsius (°C) for temperature measurement
        """
        super().__init__(
            unit = UnitOfMeasurement.CELSIUS, 
            type = SensorType.TEMPERATURE,
            **kwargs
        )
