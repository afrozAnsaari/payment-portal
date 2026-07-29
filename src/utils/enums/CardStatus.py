from enum import Enum


class CardStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    FROZEN = "FROZEN"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"
