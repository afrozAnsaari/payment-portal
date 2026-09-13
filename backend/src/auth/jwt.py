import secrets

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from jose import (
    jwt,
    JWTError,
)

SECRET_KEY = "dev_secret_change_later"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRY_IN_HRS = 1

REFRESH_TOKEN_EXPIRY_IN_DAYS = 7


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRY_IN_HRS)

    payload.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        # print("JWT Payload: ", payload)

        # print("TOKEN TYPE: ", payload.get("type"))

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None


def create_refresh_token():
    return secrets.token_urlsafe(64)
