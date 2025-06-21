from enum import Enum


class PeerType(int, Enum):
    UNKNOWN = 0
    PRIVATE = 1
    
    GROUP = 2
    """This value defines `Channels` and `Groups`"""
