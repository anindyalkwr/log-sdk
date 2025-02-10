from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class ElectricalLogData(BaseSensorLogData):
    """
    Logs electrical sensor data
    """

    def __init__(self, **kwargs):
        """
        Unit: Ampere (A) for Electrical measurement
        """
        super().__init__(
            unit = UnitOfMeasurement.AMPERE, 
            type = SensorType.ELECTRICAL,
            **kwargs
        )
