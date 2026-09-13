from enum import Enum

class AccountStatus(str,Enum):

    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    FROZEN = "FROZEN"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"