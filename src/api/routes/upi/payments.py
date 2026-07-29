from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from src.auth.verify_user import get_current_user

from src.auth.verify_payment_pin import verify_acc_pin


from src.databases.models import User

from src.databases.database import get_db

from src.schemas.payment import PaymentCreate, PaymentResponse


from src.services.fraud.predictor import predict_fraud
from src.services.fraud_service import predict_transaction
from src.utils.enums.FraudDecision import FraudDecision


from src.services.payment_service import process_payment_transaction

router = APIRouter(tags=["Payments"])


@router.post("/upi/pay")
def make_payment(
    payment: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_acc_pin(
        payment.account_pin,
        current_user,
    )

    saved_payment = process_payment_transaction(
        db=db,
        payment_data=payment,
        current_user=current_user,
    )

    return {
        "payment_id": saved_payment.id,
        "amount": saved_payment.amount,
        "status": saved_payment.status,
        "risk_score": saved_payment.risk_score,
        "fraud_decision": saved_payment.fraud_decision,
    }
