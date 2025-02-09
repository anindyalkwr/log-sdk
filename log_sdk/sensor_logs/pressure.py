from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class PressureLogData(BaseSensorLogData):
    """
    Logs pressure sensor data
    """

    def __init__(self, **kwargs):
        """
        Unit: Bar for pressure measurement
        """
        super().__init__(
            unit = UnitOfMeasurement.BAR, 
            type = SensorType.PRESSURE,
            **kwargs
        )
