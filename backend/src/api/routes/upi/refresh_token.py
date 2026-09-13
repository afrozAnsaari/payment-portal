from fastapi import APIRouter, HTTPException

from datetime import datetime, timezone

from fastapi import Depends

from sqlalchemy.orm import Session


from src.databases.refresh_token import RefreshToken

from src.databases.database import get_db

from src.schemas.refresh_token import RefreshTokenRequest

from src.auth.jwt import create_access_token

from src.security.hash_utils import sha256_hash

router = APIRouter(tags=["Refresh"])


@router.post(
    "/auth/refresh",
    responses={
        401: {
            "description": "Invalid or expired refresh token",
        },
    },
)
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    token_hash = sha256_hash(request.refresh_token)

    stored_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if stored_token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
        )

    now = datetime.now(timezone.utc)

    if stored_token.expires_at <= now:
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired. Please login again.",
        )

    access_token = create_access_token(
        {
            "user_id": stored_token.user_id,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
