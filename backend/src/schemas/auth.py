from pydantic import BaseModel, field_validator


class LoginRequest(BaseModel):

    mobile_no: str

    password: str

    @field_validator("mobile_no")
    @classmethod
    def validate_mobile_no(cls, value: str):
        if not value.isdigit() or (len(value) != 10):
            raise ValueError("Invalid Mobile Number.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not value.isdigit() or not 4 <= len(value) <= 6:
            raise ValueError("Incorrect Password")
        return value


class LogoutRequest(BaseModel):

    refresh_token: str
