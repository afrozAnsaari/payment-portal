from pydantic import BaseModel


class PaymentRequest(BaseModel):

    merchant_id: int

    type: str

    amount: float

    oldbalanceOrg: float

    newbalanceOrig: float

    oldbalanceDest: float

    newbalanceDest: float
