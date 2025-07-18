from enum import Enum


class GroupType(int, Enum):
    GROUP = 0
    CHANNEL = 1
    SUPERGROUP = 2
