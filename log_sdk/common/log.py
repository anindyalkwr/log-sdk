from datetime import datetime, timezone
import json

from log_sdk.common.action import Action, ActionType 
from log_sdk.common.channel import Channel 
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status
from log_sdk.common.type import LogType


class APMLogData:


    def __init__(self, 
                 hostname = str, 
                 ip = str, 
                 action = Action, 
                 action_type = ActionType, 
                 duration = float, 
                 channel = Channel, 
                 product = Product, 
                 data_center = DataCenter, 
                 status = Status, 
                 metadata=None
                ):
        

        self.hostname = hostname
        self.ip = ip
        self.action = action
        self.action_type = action_type
        self.duration = duration
        self.channel = channel
        self.product = product
        self.data_center = data_center
        self.status = status
        self.metadata = metadata


    def to_dict(self):


        return self.__dict__


class Log:


    def __init__(self, 
                 log_type = LogType, 
                 trace_id = str, 
                 span_id = str, 
                 data = APMLogData
                ):


        self.log_type = log_type
        self.timestamp = datetime.now(timezone.utc)
        self.trace_id = trace_id
        self.span_id = span_id
        self.data = data


    def to_dict(self):


        return {
            "log_type": self.log_type,
            "timestamp": self.timestamp.isoformat(),
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "data": self.data.to_dict(),
        }


    def save(self, logger):


        log_data = self.to_dict()
        logger.info(json.dumps(log_data))
