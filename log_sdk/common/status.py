from enum import Enum


class Status(str, Enum):

    
    OK = "OK"
    FAILED = "FAILED"
    PENDING = "PENDING"
    