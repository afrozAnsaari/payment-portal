from pydantic import BaseModel, field_validator

from src.utils.luhn import validate_card_number


class LinkBankRequest(BaseModel):

    bank_name: str

    card_number: str

    expiry_month: int

    expiry_year: int

    card_pin: str  # PIN of the said card that is to be linked to the UPIProfile acc

    # PIN of the UPIProfile that will be used to do payments in the future
    # new_upi_pin: str | None = None

    @field_validator("card_number")
    @classmethod
    def check_card_number(cls, value: str):

        # Remove spaces and hyphen
        value = value.replace(" ", "").replace("-", "")

        # Check if all character are digits
        if len(value) != 16 or not value.isdigit():
            raise ValueError("Card number must be exactly 16 digits")

        if not validate_card_number(value):
            raise ValueError("Please enter a valid card number")

        return value

    @field_validator("card_pin")
    @classmethod
    def validate_card_pin(cls, value):
        if value is None:
            return value

        if not (4 <= len(value) <= 6) or not value.isdigit():
            raise ValueError("PIN must be between 4 to 6 digits")

        return value

    # @field_validator("new_upi_pin")
    # @classmethod
    # def validate_new_upi_pin(cls, value: str):

    #     if value is None:
    #         return value

    #     if not value.isdigit() or not (4 <= len(value) <= 6):
    #         raise ValueError("UPI PIN must be 4-6 digits")

    #     return value
