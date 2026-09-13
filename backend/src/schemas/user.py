from pydantic import BaseModel, field_validator, EmailStr
import re

PHONE_REGEX = re.compile(r"^\d{10}$")


class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    password: str

    @field_validator("mobile_no")
    @classmethod
    def validate_mobile_no(cls, value: str):
        if not PHONE_REGEX.fullmatch(value):
            raise ValueError("Mobile number must contain exactly 10 digits.")
        return value
