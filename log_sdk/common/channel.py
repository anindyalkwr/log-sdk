from enum import Enum


class Channel(str, Enum):

    
    WEB_INTERFACE = "WEB-INTERFACE"
    MOBILE_INTERFACE = "MOBILE-INTERFACE"
    API_INTERFACE = "API-INTERFACE"
    DESKTOP_INTERFACE = "DESKTOP-INTERFACE"
