from enum import Enum


class Product(str, Enum):


    PRODUCT_FUNDING = "PRODUCT"
    PRODUCT_PAYMENT = "PAYMENT"
    PRODUCT_SWITCHING = "SWITCHING"
    