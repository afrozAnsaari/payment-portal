from fastapi import Depends, Header, HTTPException


from sqlalchemy.orm import Session


from src.databases.database import get_db
from src.databases.models import Merchant


def verify_api_key(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing API Key")

    api_key = authorization.replace("Bearer ", "")

    merchant = db.query(Merchant).filter(Merchant.api_key == api_key).first()

    if merchant is None:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if merchant.is_active is False:
        raise HTTPException(status_code=403, detail="Merchant disabled")

    return merchant
