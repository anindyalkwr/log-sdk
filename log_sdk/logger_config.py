from datetime import datetime, timezone
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from confluent_kafka import Producer

# Import Enums and Log Classes
from log_sdk.common.action import Action
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status
from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.sensor_logs.electrical import ElectricalLogData
from log_sdk.sensor_logs.humidity import HumidityLogData
from log_sdk.sensor_logs.pressure import PressureLogData
from log_sdk.sensor_logs.temperature import TemperatureLogData
from log_sdk.sensor_logs.vibration import VibrationLogData


class LoggerConfig:
    """
    Logger configuration that supports Kafka-based logging and optional file backup.
    """
    def __init__(
            self, 
            sensor_id: str,
            KAFKA_BOOTSTRAP_SERVERS: str,
            KAFKA_TOPIC: str,
            kafka_enabled=True,
            log_directory="./logs",
        ):
        """
        Initializes the logger.

        :param kafka_enabled: Whether to send logs to Kafka.
        :param log_directory: Directory for local log backups.
        """
        self.sensor_id = sensor_id
        self.KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS
        self.KAFKA_TOPIC = KAFKA_TOPIC
        self.kafka_enabled = kafka_enabled
        self.logger = self._init_log_file(log_directory)
        self.machine_status = None
        self.status_timestamp = None

        if self.kafka_enabled:
            self.producer = Producer({'bootstrap.servers': self.KAFKA_BOOTSTRAP_SERVERS})


    @staticmethod
    def _init_log_file(directory):
        """
        Initializes file-based logging (optional fallback).
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        log_file = os.path.join(directory, f"sensor_logs_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log")

        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=12)
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        logger = logging.getLogger("sensor_logger")
        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    

    def _calculate_time_difference(self) -> float:
        """
        Calculates the time difference between now and the last status change.

        :return: The difference in seconds.
        """
        if self.status_timestamp is None:
            return 0.0  # If no previous status, return 0 uptime/downtime
        return (datetime.now(timezone.utc) - self.status_timestamp).total_seconds()
    
    
    def _add_machine_metadata(self, metadata: Optional[dict]) -> dict:
        """
        Adds machine status, uptime, or downtime to metadata.

        :param metadata: The existing metadata dictionary.
        :return: The updated metadata dictionary.
        """
        if metadata is None:
            metadata = {}

        metadata["machine_status"] = self.machine_status.value if self.machine_status else "UNKNOWN"
        time_difference = self._calculate_time_difference()

        if self.machine_status == Action.START:
            metadata["uptime"] = time_difference
        elif self.machine_status in {Action.STOP, Action.MAINTENANCE, Action.CALIBRATION}:
            metadata["downtime"] = time_difference

        return metadata
    

    def _send_to_kafka(self, log_data):
        """
        Sends log data to Kafka.
        """
        try:
            self.producer.produce(self.KAFKA_TOPIC, value=json.dumps(log_data))
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Kafka Error: {str(e)}")


    def _log(self, log_object: BaseSensorLogData):
        """
        Logs data to Kafka and optionally to a file.
        :param log_object: A log instance (BaseSensorLog, VibrationLog, TemperatureLog, etc.)
        """
        log_data = log_object.to_dict()

        if self.kafka_enabled:
            self._send_to_kafka(log_data)

        self.logger.info(json.dumps(log_data, indent=4))

    
    def update_machine_status(self, action: Action):
        """
        Updates the machine status and records the timestamp.

        :param action: The new machine status (e.g., Start, Stop, Maintenance, Calibration).
        """
        if self.machine_status != action:
            self.machine_status = action
            self.status_timestamp = datetime.now(timezone.utc)
            self.logger.info(f"Machine status updated: {self.machine_status.value} at {self.status_timestamp}")


    def log_electrical(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs pressure electrical data (unit: Ampere).
        """
        metadata = self._add_machine_metadata(metadata)

        log = ElectricalLogData(
            sensor_id = self.sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            duration = duration,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)

    def log_humidity(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs humidity sensor data (unit: Percent).
        """
        metadata = self._add_machine_metadata(metadata)


        log = HumidityLogData(
            sensor_id = self.sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            duration = duration,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_pressure(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs pressure sensor data (unit: Bar).
        """
        metadata = self._add_machine_metadata(metadata)

        log = PressureLogData(
            sensor_id = self.sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            duration = duration,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_temperature(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs temperature sensor data (unit: °C).
        """
        metadata = self._add_machine_metadata(metadata)

        log = TemperatureLogData(
            sensor_id = self.sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            duration = duration,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_vibration(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs vibration sensor data (unit: Hz).
        """
        metadata = self._add_machine_metadata(metadata)

        log = VibrationLogData(
            sensor_id = self.sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            duration = duration,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)
