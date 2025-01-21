# Log SDK for Standardizing Logs

This SDK is designed to standardize log generation and handling across the system. It provides a consistent format for logging application metrics, transactions, and other important data. The logs can be used for monitoring, debugging, and performance tracking.

## Fields in the Logs

The SDK captures various fields that represent different log attributes:

### `APMLogData`

Contains application performance monitoring (APM) data.

- **`hostname`**: The host machine's name where the log is generated (e.g., `"example-host"`).
- **`ip`**: The IP address of the system.
- **`action`**: The type of action being logged (e.g., `Action.TRANSACTION`).
- **`action_type`**: The specific type of action, such as `ActionType.BIFAST`.
- **`duration`**: Duration of the action (in milliseconds).
- **`channel`**: The communication channel for the transaction (e.g., `Channel.WOB`).
- **`product`**: The product being acted upon (e.g., `Product.PRODUCT_FUNDING`).
- **`data_center`**: Data center information (e.g., `DataCenter.DC1`).
- **`status`**: Status of the action (e.g., `Status.OK`).
- **`metadata`**: A dictionary of additional information for custom logging (e.g., `{ "key": "value" }`).

### `Log`

Represents a single log entry.

- **`log_type`**: The type of log (e.g., `LogType.LOG_TYPE_APM`).
- **`trace_id`**: Unique trace identifier for tracking the flow of operations.
- **`span_id`**: Unique span identifier within the trace.
- **`data`**: The APMLogData instance, containing all the relevant log data.

## How to Use the SDK

1. **Initialize Logger**  
   The first step is to initialize the logger with a file handler.

   ```python
   logger = LoggerConfig.init_log_file("logs")

2. **Create Log Data**  
   You can create APM log data with various fields, including action, duration, and status.

   ```python
   apm_data = APMLogData(
       hostname="example-host",
       ip="192.168.1.1",
       action=Action.TRANSACTION,
       action_type=ActionType.BIFAST,
       duration=123,
       channel=Channel.MOBILE_INTERFACE,
       product=Product.PRODUCT_FUNDING,
       data_center=DataCenter.DC1,
       status=Status.OK,
       metadata={"key": "value"}
   )

3. **Create and Save Log**  
   After creating the log data, you can create a `Log` instance and save it to the logger.

   ```python
   log = Log(
       log_type=LogType.LOG_TYPE_APM,
       trace_id="trace-id-123",
       span_id="span-id-456",
       data=apm_data
   )
   log.save(logger)

4. **Log Rotation**  
   The SDK includes a `RotatingFileHandler` to manage log rotation. This handler will rotate logs based on size, keeping the logs manageable and ensuring old logs are archived.

   - The log file will automatically be rotated once it reaches the specified size (in this case, 10 MB).
   - The handler will keep 3 backup copies of the log file, meaning when the log reaches the maximum size, the old log will be archived and a new log file will be created.
   - This prevents log files from growing too large, ensuring efficient storage and better performance for the logging system.

## Contributing

Feel free to fork this repository and submit pull requests to improve the functionality. Please follow the code style conventions provided in the project. When contributing, please make sure to:

- Provide a clear description of your changes.
- Include tests where applicable.
- Ensure your changes do not break existing functionality.
- Update the documentation if necessary.

### Bug Reports

If you encounter any issues or bugs, please open an issue on the GitHub repository and provide as much information as possible to help us resolve the issue quickly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.