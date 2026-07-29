from enum import Enum


class FraudDecision(str, Enum):
    APPROVED = "APPROVED"

    BLOCKED = "BLOCKED"

    REVIEW = "UNDER REVIEW"
