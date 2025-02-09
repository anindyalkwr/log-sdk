from log_sdk.common.action import Action
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status


class MachineLogData:
    """
    General log for machine status, including downtime, error codes, etc.
    """

    def __init__(
            self,
            hostname: str,
            ip: str,
            action: Action,
            status: Status,
            channel: Channel,
            product: Product,
            data_center: DataCenter,
            metadata=None
        ):
        """
        :param hostname: Machine or device hostname
        :param ip: IP address of the machine
        :param status: Machine operational status
        :param channel: The data source channel
        :param product: The product line or business unit
        :param data_center: The data center or location of the machine
        :param metadata: Additional machine-specific metadata (JSON field)
        """
        self.hostname = hostname
        self.ip = ip
        self.action = action
        self.product = product
        self.data_center = data_center
        self.metadata = metadata if metadata else {}


    def to_dict(self):
        return self.__dict__
    