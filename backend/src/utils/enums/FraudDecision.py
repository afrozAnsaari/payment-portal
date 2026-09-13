from enum import Enum


class FraudDecision(str, Enum):
    APPROVED = "APPROVED"

    REVIEW = "REVIEW"

    DECLINED = "DECLINED"

    
