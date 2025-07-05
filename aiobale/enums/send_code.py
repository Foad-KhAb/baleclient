from enum import Enum


class SendCodeType(int, Enum):
    UNKNOWN = 0
    DEFAULT = 1
    BALEONLY = 2
    SMS = 3
    CALL = 4
    EMAIL = 5
    MISSCALL = 6
    SETUP_EMAIL_REQUIRED = 7
    WHATSAPP = 8
    TELEGRAM = 9
    USSD = 10
    FUTURE_AUTH_TOKEN = 11
    TELEGRAM_GATEWAY = 12
