from enum import Enum


class ReportKind(int, Enum):
    UNKNOWN = 0
    SPAM = 1
    INAPPROPRIATE_CONTENT = 2
    OTHER = 3
    VIOLENCE = 4
    SPAM = 5
    FALSE_INFORMATION = 6
