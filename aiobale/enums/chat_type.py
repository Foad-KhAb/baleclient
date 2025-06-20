from enum import Enum


class ChatType(int, Enum):
    UNKNOWN = 0
    PRIVATE = 1
    GROUP = 2
    CHANNEL = 3
    BOT = 4
    SUPRER_GROUP = 5
