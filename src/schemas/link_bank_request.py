from pydantic import BaseModel, Field, field_validator


class LinkBankRequest(BaseModel):

    upi_profile_id: int

    bank_name: str

    card_number: str

    expiry_month: int

    expiry_year: int

    pin: str | None = None

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value):
        if value is None:
            return value

        if not (4 <= len(value) <= 6) or not value.isdigit():
            raise ValueError(
                "PIN must be exactly between 4 to 6 digits and only numbers"
            )

        return value
