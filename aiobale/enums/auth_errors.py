from enum import Enum


class AuthErrors(int, Enum):
    UNKNOWN = 0
    NUMBER_BANNED = 1
    AUTH_LIMIT = 2
    WRONG_CODE = 3
    PASSWORD_NEEDED = 4
    SIGN_UP_NEEDED = 5
    WRONG_PASSWORD = 6
    RATE_LIMIT = 7
    INVALID = 8
