from enum import Enum


class PeerSource(int, Enum):
    UNKNOWN = 0
    DIALOGS = 1
    VITRINE = 2
    MARKET = 3
    PRIVACY_BAR = 4
