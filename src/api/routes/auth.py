from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)


from sqlalchemy.orm import Session

from src.databases.database import get_db

from src.databases.models import User

from src.schemas.auth import LoginRequest

from src.security.password import verify_password

from src.auth.jwt import create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.email == credentials.email).first()

    if user is None:
        raise HTTPException(
            status_code=402,
            detail="Invalid Credentials",
        )

    valid_password = verify_password(
        credentials.password,
        user.password_hash,
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid passowrd",
        )

    token = create_access_token(
        {
            "user_id": user.id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
