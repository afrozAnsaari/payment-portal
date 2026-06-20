from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.databases.database import get_db

from src.schemas.user import UserCreate

from src.databases.crud import create_user

router = APIRouter(tags=["Users"])


@router.post("/users")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    created = create_user(
        db,
        user.model_dump(),
    )

    return {
        "user_id": created.id,
        "name": created.name,
        "account_id": created.account.id
    }
