from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status
from log_sdk.common.type import SensorType
from log_sdk.common.unit import UnitOfMeasurement


class BaseSensorLogData:
    """
    Base class for all sensor logs (e.g., Vibration, Temperature, Pressure)
    """

    def __init__(
            self,
            hostname: str,
            sensor_id: str,
            measurement: float,
            channel: Channel,
            data_center: DataCenter,
            product: Product,
            status: Status,
            type: SensorType,
            unit: UnitOfMeasurement,
            metadata=None
        ):
        """
        :param hostname: Machine or device hostname
        :param sensor_id: Unique identifier for the sensor
        :param measurement: The actual value recorded by the sensor
        :param channel: The data source channel
        :param data_center: The data center or location of the machine
        :param product: The product line or business unit
        :param status: Operational status of the machine or sensor
        :param type: Type of sensor used for the measurement.
        :param unit: The unit of the measurement (e.g., Hz, °C, Bar)
        :param metadata: Additional sensor-specific metadata (JSON field)
        """
        self.hostname = hostname
        self.sensor_id = sensor_id
        self.measurement = measurement
        self.channel = channel
        self.data_center = data_center
        self.product = product
        self.status = status
        self.type = type
        self.unit = unit
        self.metadata = metadata if metadata else {}


    def to_dict(self):
        return self.__dict__
