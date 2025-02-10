from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class HumidityLogData(BaseSensorLogData):
    """
    Logs humidity sensor data
    """

    def __init__(self, **kwargs):
        """
        Unit: Percent (%) for humidity measurement
        """
        super().__init__(
            unit = UnitOfMeasurement.PERCENT, 
            type = SensorType.HUMIDITY,
            **kwargs
        )
