import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.databases.models import UPIProfile, User

PHONE_NUMBER_REGEX = re.compile(r"^[6-9]\d{9}$")

UPI_ID_REGEX = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{1,48}@[a-zA-Z.]{2,50}$")

UPI_ID_REGEX = re.compile(
    r"^[a-zA-Z0-9][a-zA-Z0-9._-]{1,48}@[a-zA-Z]+(?:\.[a-zA-Z]+)*$"
)


def resolve_receiver(db: Session, receiver: str) -> UPIProfile:

    receiver = receiver.strip()

    if UPI_ID_REGEX.fullmatch(receiver):

        profile = (
            db.query(UPIProfile)
            .filter(
                UPIProfile.upi_id == receiver,
                UPIProfile.is_active == True,
            )
            .first()
        )

    elif PHONE_NUMBER_REGEX.fullmatch(receiver):

        user = db.query(User).filter(User.mobile_no == receiver).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail=" Please verify the details you have mentioned again.",
            )

        profile = (
            db.query(UPIProfile)
            .filter(
                UPIProfile.user_id == user.id,
                UPIProfile.is_active == True,
            )
            .first()
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Receiver must be a valid UPI ID or a 10-digit mobile number.",
        )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Receiver UPI profile not found.",
        )

    return profile
