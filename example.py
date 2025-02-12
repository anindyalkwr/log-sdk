import time
from log_sdk.logger_config import LoggerConfig
from log_sdk.common.action import Action
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status

logger = LoggerConfig(
    sensor_id="sensor-1234",
    KAFKA_BOOTSTRAP_SERVERS="localhost:9092",
    KAFKA_TOPIC="sensor_logs",
    kafka_enabled=True,
    log_directory="./logs"
)

logger.update_machine_status(Action.START)
time.sleep(2)

logger.log_vibration(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=2.0,
    measurement=4.5,  # Hz
    product=Product.MACHINE_MONITORING,
    status=Status.NORMAL
)

time.sleep(1)

logger.log_temperature(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=1.5,
    measurement=75.2,  # °C
    product=Product.MACHINE_MONITORING,
    status=Status.NORMAL
)

time.sleep(2)

logger.update_machine_status(Action.MAINTENANCE)
time.sleep(3)

logger.log_pressure(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=3.0,
    measurement=2.3,
    product=Product.MACHINE_MONITORING,
    status=Status.WARNING
)

time.sleep(1)

logger.update_machine_status(Action.STOP)
time.sleep(2)

logger.log_electrical(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=2.0,
    measurement=12.5,
    product=Product.MACHINE_MONITORING,
    status=Status.CRITICAL
)

time.sleep(1)

logger.log_humidity(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=1.0,
    measurement=55.8,  # %
    product=Product.MACHINE_MONITORING,
    status=Status.NORMAL
)

print("Example logging complete. Check ./logs for the log file.")
