from enum import Enum


class Services(str, Enum):
    MESSAGING = "bale.messaging.v2.Messaging"
    AUTH = "bale.auth.v1.Auth"
