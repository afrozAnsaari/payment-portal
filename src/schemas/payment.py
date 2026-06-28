from pydantic import BaseModel


class PaymentRequest(BaseModel):

    type: str

    # sender_account_id: int

    receiver_account_id: int

    amount: float

    oldbalanceOrg: float

    newbalanceOrig: float

    oldbalanceDest: float

    newbalanceDest: float

    payment_pin: str
