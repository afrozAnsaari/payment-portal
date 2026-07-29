from pydantic import BaseModel

from src.utils.enums.CardNetwork import CardNetwork

class CardCreate(BaseModel):

    account_id: int

    network: CardNetwork

