from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str

    email: str

    initial_balance: float = 0
