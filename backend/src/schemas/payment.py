from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator


class PaymentCreate(BaseModel):

    model_config = ConfigDict(frozen=True)

    receiver: str = Field(
        ...,
        description="Receiver mobile number or UPI ID",
    )

    sender_upi_profile_id: int = Field(
        ...,
        description="UPI Profile of the sender used to initiate the payment",
    )

    sender_account_id: int = Field(
        ...,
        description="Linked Bank Account used to fund payment",
    )

    amount: int = Field(
        ...,
        description="Amount to be transferred",
    )

    upi_pin: str = Field(
        ...,
    )

    @field_validator("upi_pin")
    @classmethod
    def validate_upi_pin(cls, value: str):

        if not value.isdigit() or not (4 <= len(value) <= 6):
            raise ValueError("UPI PIN must be 4-6 digits.")

        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: int):

        if value <= 0:
            raise ValueError("Amount should be greater than zero")
        return value


class PaymentResponse(BaseModel):
    transaction_id: str
    amount: float
    status: str
    receiver: str
    transaction_type: str
    created_at: datetime
    message: str

    model_config = {"from_attributes": True}
