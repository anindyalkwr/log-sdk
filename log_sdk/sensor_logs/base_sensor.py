from datetime import datetime, timezone
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
            sensor_id: str,
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float,
            product: Product,
            status: Status,
            type: SensorType,
            unit: UnitOfMeasurement,
            metadata=None
        ):
        """
        :param sensor_id: Unique identifier for the sensor
        :param channel: The data source channel
        :param data_center: The data center or location of the machine
        :param duration: The time in seconds for which this measurement was recorded
        :param measurement: The actual value recorded by the sensor
        :param product: The product line or business unit
        :param status: The status of the sensor data
        :param type: Type of sensor used for the measurement.
        :param unit: The unit of the measurement (e.g., Hz, °C, Bar)
        :param metadata: Additional sensor-specific metadata (JSON field)
        """
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.sensor_id = sensor_id
        self.channel = channel
        self.data_center = data_center
        self.duration = duration
        self.measurement = measurement
        self.product = product
        self.status = status
        self.type = type
        self.unit = unit
        self.metadata = metadata if metadata else {}


    def to_dict(self):
        """
        Converts the log object to a dictionary, ensuring Enums are serialized as strings.
        """
        return {
            "timestamp": self.timestamp,
            "sensor_id": self.sensor_id,
            "channel": self.channel.value,
            "data_center": self.data_center.value,
            "duration": self.duration,
            "measurement": self.measurement,
            "product": self.product.value,
            "status": self.status.value,
            "type": self.type.value,
            "unit": self.unit.value,
            "metadata": self.metadata
        }
