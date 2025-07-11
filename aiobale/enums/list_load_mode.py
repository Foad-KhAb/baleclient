from enum import Enum


class ListLoadMode(int, Enum):
    UNKNOWN = 0
    FORWARD = 1
    BACKWARD = 2
    BOTH = 3
