from enum import Enum


class GiftOpenning(int, Enum):
    ALREADY_RECEIVED = 0
    SOLD_OUT = 1
    GIFT_CREATOR = 2
    SUCCESSFUL = 3
    PENDING = 4
