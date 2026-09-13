from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from src.databases.database import get_db
from src.databases.refresh_token import RefreshToken
from src.schemas.auth import LogoutRequest
from src.security.hash_utils import sha256_hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/logout",
    responses={
        401: {
            "description": "Invalid or already revoked refresh token",
        },
    },
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
):
    token_hash = sha256_hash(request.refresh_token)

    stored_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
        )
        .first()
    )

    if stored_token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
        )

    if stored_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="Refresh token already revoked.",
        )

    stored_token.revoked = True

    db.commit()

    return {
        "message": "Logged out successfully.",
    }
