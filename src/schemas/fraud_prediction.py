from pydantic import BaseModel


class FraudPrediction(BaseModel):
    risk_score: float
    decision: str
