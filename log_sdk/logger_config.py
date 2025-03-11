from logging.handlers import RotatingFileHandler
from typing import Optional, Type
from datetime import datetime, timezone

import json
import logging
import os

from fogverse import KafkaProducer

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

        :param sensor_id: Unique identifier for the sensor.
        :param KAFKA_BOOTSTRAP_SERVERS: Kafka bootstrap servers.
        :param KAFKA_TOPIC: Kafka topic to publish logs to.
        :param kafka_enabled: Boolean flag indicating whether to send logs to Kafka.
        :param log_directory: Directory path for local log backups.
        """
        self.sensor_id = sensor_id

        # Due to the current configuration of Fogverse Producer, Kafka bootstrap servers and topic are not used
        # since the values are directly loaded from environment variables.       
        self.KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS
        self.KAFKA_TOPIC = KAFKA_TOPIC

        self.kafka_enabled = kafka_enabled
        self.logger = self._init_log_file(log_directory)
        self.machine_status = None
        self.status_timestamp = None

        if self.kafka_enabled:
            self.producer = KafkaProducer(
                topic= KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
            )


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

        logger = logging.getLogger("sensor_logger")
        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger
    

    def _calculate_time_difference(self) -> float:
        """
        Calculates the time difference between now and the last status change.

        :return: The difference in seconds.
        """
        if self.status_timestamp is None:
            return 0.0 
            
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
    

    async def _send_to_kafka(self, log_data):
        """
        Sends log data to Kafka.
        """
        try:
            await self.producer._send(json.dumps(log_data).encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Kafka Error: {str(e)}")


    async def _log(self, log_object: BaseSensorLogData):
        """
        Logs data to Kafka and optionally to a file.
        
        :param log_object: A log instance (BaseSensorLog, VibrationLog, TemperatureLog, etc.)
        """
        log_data = log_object.to_dict()

        if self.kafka_enabled:
            await self._send_to_kafka(log_data)

        self.logger.info(json.dumps(log_data, indent=4))


    async def _generic_sensor_log(
            self,
            log_cls: Type[BaseSensorLogData],
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None,
        ):
        """
        A generic method to log sensor data, reducing redundancy across log methods.

        :param log_cls: The log data class to instantiate (e.g., ElectricalLogData).
        :param channel: The channel of the sensor.
        :param data_center: The data center.
        :param duration: Duration of the measurement.
        :param measurement: The sensor measurement.
        :param product: The product associated with the measurement.
        :param status: The status of the sensor.
        :param metadata: Optional additional metadata.
        """
        metadata = self._add_machine_metadata(metadata)
        log = log_cls(
            sensor_id=self.sensor_id,
            measurement=measurement,
            channel=channel,
            data_center=data_center,
            duration=duration,
            product=product,
            status=status,
            metadata=metadata,
        )
        await self._log(log)

    async def log_electrical(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None
        ):
        """
        Logs electrical sensor data (unit: Ampere).
        """
        await self._generic_sensor_log(ElectricalLogData, channel, data_center, duration, measurement, product, status, metadata)

    async def log_humidity(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None
        ):
        """
        Logs humidity sensor data (unit: Percent).
        """
        await self._generic_sensor_log(HumidityLogData, channel, data_center, duration, measurement, product, status, metadata)

    async def log_pressure(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None
        ):
        """
        Logs pressure sensor data (unit: Bar).
        """
        await self._generic_sensor_log(PressureLogData, channel, data_center, duration, measurement, product, status, metadata)

    async def log_temperature(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None
        ):
        """
        Logs temperature sensor data (unit: °C).
        """
        await self._generic_sensor_log(TemperatureLogData, channel, data_center, duration, measurement, product, status, metadata)

    async def log_vibration(
            self, 
            channel: Channel,
            data_center: DataCenter,
            duration: float,
            measurement: float, 
            product: Product,
            status: Status,
            metadata: Optional[dict] = None
        ):
        """
        Logs vibration sensor data (unit: Hz).
        """
        await self._generic_sensor_log(VibrationLogData, channel, data_center, duration, measurement, product, status, metadata)

        
    def update_machine_status(self, action: Action):
        """
        Updates the machine status and records the timestamp.

        :param action: The new machine status (e.g., Start, Stop, Maintenance, Calibration).
        """
        if self.machine_status != action:
            self.machine_status = action
            self.status_timestamp = datetime.now(timezone.utc)
            self.logger.info(f"Machine status updated: {self.machine_status.value} at {self.status_timestamp}")


    async def initialize(self):
        """
        Initialize the Kafka producer.
        """
        if self.kafka_enabled:
            await self.producer.start()


    async def close(self):
        """
        Close the Kafka producer.
        """
        if self.kafka_enabled:
            await self.producer.stop()
