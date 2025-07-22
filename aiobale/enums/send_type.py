from enum import Enum


class SendType(int, Enum):
    UNKNOWN = 0
    PHOTO = 1
    VIDEO = 2
    VOICE = 3
    GIF = 4
    AUDIO = 5
    DOCUMENT = 6
    STICKER = 7
    CROWDFUNDING = 8
