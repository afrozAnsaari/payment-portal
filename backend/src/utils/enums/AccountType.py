from pydantic import BaseModel

from enum import Enum



class AccountType(str, Enum):

    SAVINGS = "SAVINGS"

    CURRENT = "CURRENT"
