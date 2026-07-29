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

ACCESS_TOKEN_EXPIRY_IN_MIN = 60


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_IN_MIN)

    payload.update({"exp": expire})

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

        return payload

    except JWTError:
        return None
