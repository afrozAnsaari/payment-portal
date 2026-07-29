from pydantic import BaseModel, Field

from datetime import datetime

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    receiver: str = Field(
        ...,
        description="Receiver mobile number or UPI ID",
    )
    amount: float = Field(gt=0)
    account_pin: str


class PaymentResponse(BaseModel):
    payment_id: int
    amount: float
    status: str
    receiver: str
    transaction_type: str
    created_at: datetime
    message: str

    model_config = {"from_attributes": True}
