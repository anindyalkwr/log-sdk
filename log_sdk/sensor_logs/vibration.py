from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class VibrationLogData(BaseSensorLogData):
    """
    Logs vibration sensor data
    """

    def __init__(self, **kwargs):
        """
        Unit: Hertz (Hz) for vibration frequency measurement
        """
        super().__init__(
            unit = UnitOfMeasurement.HERTZ, 
            type = SensorType.VIBRATION,
            **kwargs
        )
