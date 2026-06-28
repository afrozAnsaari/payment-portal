from fastapi import HTTPException

from src.security.password import verify_password

from src.databases.models import User


def verify_payment_pin(
    entered_pin: str,
    user: User,
):

    if user.payment_pin_hash is None:
        raise HTTPException(
            status_code=403,
            detail="Payment PIN not set",
        )

    if not verify_password(entered_pin, user.payment_pin_hash):
        raise HTTPException(
            status_code=403,
            detail="Invalid Payment PIN",
        )
