from pydantic import (
    BaseModel,
    Field,
)


from pydantic import BaseModel, Field, field_validator


class SetPinRequest(BaseModel):

    pin: str = Field(
        min_length=4,
        max_length=6,
    )

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str):
        if not value.isdigit():
            raise ValueError("PIN must contain only digits")
        return value


class VerifyPinRequest(BaseModel):

    pin: str


class BalanceRequest(BaseModel):
    pin: str
