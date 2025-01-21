from enum import Enum


class Action(str, Enum):


    TRANSACTION = "TRANSACTION"
    

class ActionType(str, Enum):

    
    BIFAST = "BIFAST"
    SKN = "SKN"
    RTGS = "RTGS"
    SWIFT = "SWIFT"
    ONLINE_TRANSFER = "ONLINE-TRANSFER"
    PAYMENT_PURCHASE = "PAYMENT/PURCHASE"
    QRIS = "QRIS"
