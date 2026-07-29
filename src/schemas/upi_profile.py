from pydantic import BaseModel


class UPIProfileCreate(BaseModel):

    user_id: int

    upi_id: str
