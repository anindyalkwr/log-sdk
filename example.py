import asyncio
import time

from log_sdk.logger_config import LoggerConfig
from log_sdk.common.action import Action
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status

async def main():
    logger = LoggerConfig(
        sensor_id="sensor-1234",
        # Due to the current configuration of Fogverse Producer, Kafka bootstrap servers and topic are not used
        # since the values are directly loaded from environment variables.
        KAFKA_BOOTSTRAP_SERVERS="localhost:9094",
        KAFKA_TOPIC="sensor_logs",
        kafka_enabled=True,
        log_directory="./logs"
    )

    await logger.initialize()

    logger.update_machine_status(Action.START)
    time.sleep(5)

    await logger.log_vibration(
        channel=Channel.SENSOR,
        data_center=DataCenter.FACTORY_1,
        duration=2.0,
        measurement=4.5,  # Hz
        product=Product.MACHINE_MONITORING,
        status=Status.NORMAL
    )

    time.sleep(5)

    await logger.log_temperature(
        channel=Channel.SENSOR,
        data_center=DataCenter.FACTORY_1,
        duration=1.5,
        measurement=75.2,  # °C
        product=Product.MACHINE_MONITORING,
        status=Status.NORMAL
    )

    logger.update_machine_status(Action.MAINTENANCE)
    time.sleep(3)

    await logger.log_pressure(
        channel=Channel.SENSOR,
        data_center=DataCenter.FACTORY_1,
        duration=3.0,
        measurement=2.3,
        product=Product.MACHINE_MONITORING,
        status=Status.WARNING
    )

    logger.update_machine_status(Action.STOP)
    time.sleep(2)

    await logger.log_electrical(
        channel=Channel.SENSOR,
        data_center=DataCenter.FACTORY_1,
        duration=2.0,
        measurement=12.5,
        product=Product.MACHINE_MONITORING,
        status=Status.CRITICAL
    )

    time.sleep(5)

    await logger.log_humidity(
        channel=Channel.SENSOR,
        data_center=DataCenter.FACTORY_1,
        duration=1.0,
        measurement=55.8,  # %
        product=Product.MACHINE_MONITORING,
        status=Status.NORMAL
    )

    print("Example logging complete. Check ./logs for the log file.")

    await logger.close()

if __name__ == "__main__":
    asyncio.run(main())
