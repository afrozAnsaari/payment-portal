from pydantic import (
    BaseModel,
)


from pydantic import BaseModel, Field, field_validator


class SetPinRequest(BaseModel):

    pin: str

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str):
        if not value.isdigit() or not (4 <= len(value) <= 6):
            raise ValueError("PIN must contain 4-6 digits digits")
        return value


class VerifyPinRequest(BaseModel):

    pin: str


class BalanceRequest(BaseModel):

    upi_profile_id: int

    account_id: int

    upi_pin: str
