from pydantic import BaseModel, Field


class UserCreate(BaseModel):

    name: str

    mobile_no: str

    email: str

    password: str
