from enum import Enum


class Services(str, Enum):
    MESSAGING = "bale.messaging.v2.Messaging"
    AUTH = "bale.auth.v1.Auth"
    USER = "bale.users.v1.Users"
    PRESENCE = "bale.presence.v1.Presence"
    REPORT = "bale.report.v1.Report"
    CONFIGS = "bale.v1.Configs"
    ABACUS = "bale.abacus.v1.Abacus"
