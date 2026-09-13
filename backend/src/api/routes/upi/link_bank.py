from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.verify_user import get_current_user

from src.databases.database import get_db
from src.databases.crud import link_bank_acc
from src.databases.models import User

from src.schemas.link_bank_request import LinkBankRequest

router = APIRouter(
    prefix="/upi",
    tags=["UPI"],
)


@router.post("/link-bank")
def link_bank(
    data: LinkBankRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return link_bank_acc(data, db, current_user)
