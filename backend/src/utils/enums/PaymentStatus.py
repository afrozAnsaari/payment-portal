from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "PENDING"

    SUCCESS = "SUCCESS"

    DECLINED = "DECLINED"

    FRAUD_BLOCKED = "FRAUD_BLOCKED"
