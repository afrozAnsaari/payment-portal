from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from src.auth.verify_user import get_current_user

from src.databases.database import get_db

from src.databases.models import User

from src.schemas.pin import SetPinRequest

from src.security.password import hash_password


from sqlalchemy.orm import Session

router = APIRouter(tags=["PIN"])


@router.post("/set-pin")
def set_pin(
    data: SetPinRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user.payment_pin_hash = hash_password(data.pin)

    db.commit()

    return {"message": "PIN created successfully"}
