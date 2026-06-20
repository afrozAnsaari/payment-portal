from fastapi import (
    Depends,
    Header,
    HTTPException,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from sqlalchemy.orm import Session


from src.databases.database import get_db
from src.databases.models import Merchant

security = HTTPBearer()


def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Merchant:

    api_key=credentials.credentials
    merchant = (db.query(Merchant)
                .filter(
                    Merchant.api_key == api_key
                    )
                .first()
                )

    if merchant is None:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if merchant.is_active is False:
        raise HTTPException(status_code=403, detail="Merchant disabled")

    return merchant
