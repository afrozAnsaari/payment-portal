import json

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
)

from sqlalchemy.orm import Session

from src.auth.verify_user import get_current_user

from src.auth.verify_payment_pin import verify_payment_pin

from src.auth.verify_api_key import verify_api_key

from src.databases.models import Merchant, User

from src.security.rate_limitter import check_rate_limit

from src.security.password import verify_password


from src.databases.database import get_db

from src.schemas.payment import PaymentRequest


from src.services.fraud.predictor import predict_fraud

from src.cache.redis_client import redis_client

from src.services.payment_service import process_payment_transaction

router = APIRouter(tags=["Payments"])


@router.post("/payments")
def make_payments(
    payment: PaymentRequest,
    user: User = Depends(get_current_user),
    idempotency_key: str = Header(None),
    merchant: Merchant = Depends(verify_api_key),
    db: Session = Depends(get_db),
):

    verify_payment_pin(
        payment.payment_pin,
        user,
    )
    redis_key = None
    cached_response = None
    if idempotency_key:
        redis_key = f"idempotency:{merchant.id}:{idempotency_key}"

        cached_response = redis_client.get(redis_key)

    if cached_response:
        print("IDEMPOTENCY HIT")
        return json.loads(cached_response)

    check_rate_limit(merchant_id=int(merchant.id))

    payment_dict = payment.model_dump()

    payment_dict["sender_account_id"] = user.account.id

    payment_dict["merchant_id"] = merchant.id

    payment_dict = payment.model_dump()

    payment_dict["sender_account_id"] = user.account.id

    payment_dict["merchant_id"] = merchant.id

    fraud_data = payment_dict.copy()

    fraud_data.pop(
        "payment_pin",
        None,
    )

    fraud_data.pop(
        "sender_account_id",
        None,
    )

    fraud_data.pop(
        "receiver_account_id",
        None,
    )

    fraud_data.pop(
        "merchant_id",
        None,
    )

    fraud_result = predict_fraud(fraud_data)
    saved_payment = process_payment_transaction(
        db,
        payment_dict,
        fraud_result,
    )

    response = {
        "payment_id": saved_payment.id,
        "amount": saved_payment.amount,
        "risk_score": fraud_result["risk_score"],
        "decision": fraud_result["decision"],
    }

    if redis_key:
        redis_client.setex(redis_key, 84600, json.dumps(response))
    return response
