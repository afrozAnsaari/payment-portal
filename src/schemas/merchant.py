from pydantic import BaseModel


class MerchantCreate(BaseModel):
    name: str
