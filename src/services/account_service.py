from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.databases.models import LinkedBankAccount
from src.databases.models import Account


def get_primary_account(
    db: Session,
    upi_profile_id: int,
) -> Account:

    linked_account = (
        db.query(LinkedBankAccount)
        .filter(
            LinkedBankAccount.upi_profile_id == upi_profile_id,
            LinkedBankAccount.is_primary == True,
        )
        .first()
    )

    if not linked_account:
        raise HTTPException(
            status_code=404,
            detail="Primary bank account not found.",
        )

    return linked_account.account
