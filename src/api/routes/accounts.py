from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from src.databases.database import get_db

from src.databases.crud import get_account_balance

router = APIRouter(tags=["Accounts"])


@router.get("/accounts/{account_id}/balance")
def balance(account_id: int, db: Session = Depends(get_db)):
    account = get_account_balance(
        db,
        account_id,
    )

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return {
        "account_id": account.id,
        "balance": account.balance,
    }
