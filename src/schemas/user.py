from pydantic import (
    BaseModel,
    Field,
)


class UserCreate(BaseModel):
    name: str

    email: str

    initial_balance: float = 0

    password: str = Field(
        min_length=8,
        max_length=16,
    )
