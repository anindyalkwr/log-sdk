from datetime import datetime, timezone
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import List


from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status
from log_sdk.sensor_logs.base_sensor import BaseSensorLogData
from log_sdk.sensor_logs.machine import MachineLogData
from log_sdk.sensor_logs.pressure import PressureLogData
from log_sdk.sensor_logs.temperature import TemperatureLogData
from log_sdk.sensor_logs.vibration import VibrationLogData


class LoggerConfig:
    """
    Logger configuration that supports Kafka-based logging and optional file backup.
    """

    def __init__(
            self, 
            KAFKA_BROKERS: List[str],
            KAFKA_TOPIC: str,
            kafka_enabled=True, 
            log_directory="./logs"
        ):
        """
        Initializes the logger.

        :param kafka_enabled: Whether to send logs to Kafka.
        :param log_directory: Directory for local log backups.
        """
        self.kafka_enabled = kafka_enabled
        self.KAFKA_BROKERS = KAFKA_BROKERS
        self.KAFKA_TOPIC = KAFKA_TOPIC
        self.logger = self._init_log_file(log_directory)

        if self.kafka_enabled:
            self.producer = Producer({'bootstrap.servers': self.KAFKA_BROKERS})


    @staticmethod
    def _init_log_file(directory):
        """
        Initializes file-based logging (optional fallback).
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        log_file = os.path.join(directory, f"sensor_logs_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log")
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=24)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        handler.setFormatter(formatter)
        logger = logging.getLogger("sensor_logger")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger
    

    def _send_to_kafka(self, log_data):
        """
        Sends log data to Kafka.
        """
        try:
            self.producer.produce(self.KAFKA_TOPIC, value=json.dumps(log_data))
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Kafka Error: {str(e)}")


    def _log(self, log_object: BaseSensorLogData | MachineLogData):
        """
        Logs data to Kafka and optionally to a file.
        :param log_object: A log instance (BaseSensorLog, VibrationLog, TemperatureLog, etc.)
        """
        log_data = log_object.to_dict()

        if self.kafka_enabled:
            self._send_to_kafka(log_data)

        self.logger.info(json.dumps(log_data, indent=4))


    def log_vibration(
            self, 
            hostname: str,
            sensor_id: str, 
            measurement: float, 
            channel: Channel,
            data_center: DataCenter,
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs vibration sensor data (unit: Hz).
        """
        log = VibrationLogData(
            hostname = hostname,
            sensor_id = sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_temperature(
            self, 
            hostname: str,
            sensor_id: str, 
            measurement: float, 
            channel: Channel,
            data_center: DataCenter,
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs temperature sensor data (unit: °C).
        """
        log = TemperatureLogData(
            hostname = hostname,
            sensor_id = sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_pressure(
            self, 
            hostname: str,
            sensor_id: str, 
            measurement: float, 
            channel: Channel,
            data_center: DataCenter,
            product: Product,
            status: Status,
            metadata=None
        ):
        """
        Logs pressure sensor data (unit: Bar).
        """
        log = PressureLogData(
            hostname = hostname,
            sensor_id = sensor_id,
            measurement = measurement,
            channel = channel,
            data_center = data_center,
            product = product,
            status = status,
            metadata = metadata,
        )
        self._log(log)


    def log_machine_status(
            self, 
            machine_id, 
            error_code, 
            status, 
            trace_id, 
            span_id, 
            metadata=None
        ):
        """
        Logs machine operational status (errors, downtime, etc.).
        """
        log = MachineLogData(
            machine_id = machine_id,
            error_code = error_code,
            status = status,
            trace_id = trace_id,
            span_id = span_id,
            metadata = metadata
        )
        self._log(log)
