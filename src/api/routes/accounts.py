from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from src.schemas.pin import BalanceRequest

from src.databases.database import get_db

from src.databases.models import (
    User,
    Account,
)

from src.auth.verify_payment_pin import verify_payment_pin

from src.security.password import verify_password

from src.auth.verify_user import get_current_user

router = APIRouter(tags=["Accounts"])


@router.post("/accounts/balance")
def get_balance(
    request: BalanceRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_payment_pin(request.pin, user)

    account = db.query(Account).filter(Account.user_id == user.id).first()

    if account is None:
        raise HTTPException(status_code=404, detail="Account missing")

    return {
        "account_id": account.id,
        "balance": account.balance,
    }
