from pydantic import (
    BaseModel,
    Field,
)


class SetPinRequest(BaseModel):

    pin: str = Field(
        min_length=4,
        max_length=8,
    )


class VerifyPinRequest(BaseModel):

    pin: str


class BalanceRequest(BaseModel):
    pin: str
