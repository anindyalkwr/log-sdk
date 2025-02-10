# Log SDK Documentation

## Overview
The **Log SDK** is designed for structured logging of sensor data from industrial systems. It supports multiple sensor types, maintains machine status, and provides optional Kafka integration for scalable data streaming.

## Features
- **Structured Logging**: Supports multiple sensor types (vibration, temperature, pressure, etc.).
- **Machine Status Tracking**: Logs `uptime` and `downtime` automatically.
- **Flexible Storage**: Logs can be sent to Kafka or stored locally.
- **Metadata Support**: Additional machine-related information is stored dynamically.

---

## **Installation**
To install the SDK:
```bash
pip install git+https://github.com/anindyalkwr/log-sdk.git
```

---

## **Enums Overview**
### **1. Action**
Defines machine actions.
```python
class Action(Enum):
    START = "Start"
    STOP = "Stop"
    MAINTENANCE = "Maintenance"
    ERROR_DETECTED = "Error Detected"
    RESET = "Reset"
    CALIBRATION = "Calibration"
```

### **2. Channel**
Defines the source of sensor logs.
```python
class Channel(Enum):
    SENSOR = "Sensor"
    SYSTEM = "System"
    MANUAL_INPUT = "Manual Input"
    ALERT = "Alert"
```

### **3. DataCenter**
Defines different factory locations.
```python
class DataCenter(Enum):
    FACTORY_1 = "Factory 1"
    FACTORY_2 = "Factory 2"
    WAREHOUSE = "Warehouse"
```

### **4. Product**
Defines monitored industrial products.
```python
class Product(Enum):
    MACHINE_MONITORING = "Machine Monitoring"
    POWER_PLANT = "Power Plant"
    OIL_AND_GAS = "Oil and Gas"
```

### **5. Status**
Defines sensor or machine status.
```python
class Status(Enum):
    NORMAL = "Normal"
    WARNING = "Warning"
    CRITICAL = "Critical"
    FAULT = "Fault"
    OFFLINE = "Offline"
```

### **6. SensorType**
Defines the type of sensor being logged.
```python
class SensorType(Enum):
    VIBRATION = "Vibration Sensor"
    TEMPERATURE = "Temperature Sensor"
    PRESSURE = "Pressure Sensor"
```

### **7. UnitOfMeasurement**
Defines measurement units for sensors.
```python
class UnitOfMeasurement(Enum):
    HERTZ = "Hz"
    CELSIUS = "°C"
    BAR = "Bar"
    PERCENT = "%"
```

---

## **Usage Guide**
### **1. Initialize Logger**
```python
from log_sdk.logger_config import LoggerConfig

logger = LoggerConfig(
    sensor_id="sensor-001",
    KAFKA_BROKERS=["localhost:9092"],
    KAFKA_TOPIC="sensor_logs",
    kafka_enabled=False,  # Logs will be saved locally
    log_directory="./logs"
)
```

### **2. Update Machine Status**
```python
from log_sdk.common.action import Action

logger.update_machine_status(Action.START)  # Machine started
```

### **3. Log Sensor Data**
#### **Logging Vibration Data**
```python
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status

logger.log_vibration(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=2.0,
    measurement=4.5,
    product=Product.MACHINE_MONITORING,
    status=Status.NORMAL
)
```

#### **Logging Temperature Data**
```python
logger.log_temperature(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=1.5,
    measurement=75.2,
    product=Product.MACHINE_MONITORING,
    status=Status.NORMAL
)
```

#### **Logging Pressure Data**
```python
logger.log_pressure(
    channel=Channel.SENSOR,
    data_center=DataCenter.FACTORY_1,
    duration=3.0,
    measurement=2.3,
    product=Product.MACHINE_MONITORING,
    status=Status.WARNING
)
```

### **4. Stop Machine and Log Downtime**
```python
logger.update_machine_status(Action.STOP)
```

---

## **Log Storage and Kafka Integration**
### **1. Log File Format (Local Storage)**
When `kafka_enabled=False`, logs are stored in `./logs/sensor_logs_YYYY-MM-DD.log`.
Example log entry:
```json
{
    "timestamp": "2025-02-10T05:07:22.099105+00:00",
    "sensor_id": "sensor-001",
    "channel": "Sensor",
    "data_center": "Factory 1",
    "duration": 2.0,
    "measurement": 4.5,
    "product": "Machine Monitoring",
    "status": "Normal",
    "metadata": {
        "machine_status": "Start",
        "uptime": 2.010275
    }
}
```

### **2. Kafka Integration**
If `kafka_enabled=True`, logs are streamed to Kafka:
```python
logger = LoggerConfig(
    sensor_id="sensor-001",
    KAFKA_BROKERS=["kafka1:9092", "kafka2:9093"],
    KAFKA_TOPIC="machine_logs",
    kafka_enabled=True
)
```

---

## **Summary**
- ✅ Supports multiple sensor types and industrial applications.
- ✅ Tracks `uptime/downtime` automatically based on machine status.
- ✅ Stores logs locally (`kafka_enabled=False`) or streams to Kafka (`kafka_enabled=True`).
- ✅ Provides structured logging for analysis and monitoring.

🚀 **Ready to use! Start logging sensor data now!** 🚀

