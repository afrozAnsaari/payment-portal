from pydantic import BaseModel, field_validator

from src.utils.enums.CardNetwork import CardNetwork


class CardCreate(BaseModel):

    account_id: int

    network: CardNetwork

    card_pin: str

    @classmethod
    @field_validator("card_pin")
    def validate_card_pin(cls, value: str):

        if not value.isdigit() and not len(value) != 4:
            raise ValueError("Card PIN must be 4 digits only")

        return value
