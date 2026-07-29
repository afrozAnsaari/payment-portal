from pydantic import BaseModel


from src.utils.enums.BankName import BankName

from src.utils.enums.AccountType import AccountType


class AccountCreate(BaseModel):

    customer_id: int

    bank_name: BankName

    account_type: AccountType

    initial_balance: float
