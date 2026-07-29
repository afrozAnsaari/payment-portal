from pydantic import BaseModel, Field


class LoginRequest(BaseModel):

    mobile_no: str = Field(min_length=10, max_length=10)

    password: str
