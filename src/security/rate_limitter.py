from fastapi import HTTPException


from src.cache.redis_client import redis_client

LIMIT = 10
WINDOW = 60


def check_rate_limit(merchant_id: int):
    key = f"rate_limit:merchant:{merchant_id}"

    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.setex(key, WINDOW, 1)

        return True

    current_count = int(current_count)

    if current_count >= LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    redis_client.incr(key)

    return True
