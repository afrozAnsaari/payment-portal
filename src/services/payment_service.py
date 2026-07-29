from fastapi import HTTPException

from src.databases.models import LedgerEntry, Payment, User, UPIProfile

from src.auth.verify_user import get_current_user

from src.schemas.payment import PaymentCreate
from src.schemas.fraud_prediction import FraudPrediction


from src.services.input_validator import resolve_receiver
from src.services.account_service import get_primary_account
from src.services.fraud_service import predict_transaction

from src.utils.enums.FraudDecision import FraudDecision
from src.utils.enums.PaymentStatus import PaymentStatus

from src.security.password import verify_password


def process_payment_transaction(
    db,
    payment_data: PaymentCreate,
    current_user: User,
):

    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Please enter a valid amount")

    try:

        sender_profile = (
            db.query(UPIProfile)
            .filter(
                UPIProfile.user_id == current_user.id,
                UPIProfile.is_active == True,
            )
            .first()
        )

        receiver_profile = resolve_receiver(
            db,
            payment_data.receiver,
        )

        if sender_profile.id == receiver_profile.id:
            raise HTTPException(
                status_code=400,
                detail="Money cannot be transferred to the same account.",
            )

        sender_acc = get_primary_account(db, sender_profile.id)

        receiver_acc = get_primary_account(db, receiver_profile.id)

        if sender_acc.balance < payment_data.amount:
            raise HTTPException(
                status_code=404, detail="Insufficient Balance. Transaction Denied"
            )

        fraud_prediction: FraudPrediction = predict_transaction(
            sender_account=sender_acc,
            receiver_account=receiver_acc,
            amount=payment_data.amount,
            transaction_type="P2P",
        )

        fraud_decision = fraud_prediction.decision

        if fraud_decision == FraudDecision.DECLINED.value:
            raise HTTPException(
                status_code=403,
                detail="Your transaction has been declined due to being in the risk zone. Please try again later...",
            )

        sender_acc.balance -= payment_data.amount

        receiver_acc.balance += payment_data.amount

        payment = Payment(
            sender_upi_profile_id=sender_profile.id,
            receiver_upi_profile_id=receiver_profile.id,
            sender_account_id=sender_acc.id,
            receiver_account_id=receiver_acc.id,
            amount=payment_data.amount,
            transaction_type="P2P",
            status=PaymentStatus.SUCCESS.value,
            risk_score=fraud_prediction.risk_score,
            fraud_decision=fraud_decision,
        )

        db.add(payment)
        db.flush()

        debit = LedgerEntry(
            payment_id=payment.id,
            account_id=sender_acc.id,
            entry_type="DEBIT",
            amount=payment.amount,
        )

        credit = LedgerEntry(
            payment_id=payment.id,
            account_id=receiver_acc.id,
            entry_type="CREDIT",
            amount=payment.amount,
        )

        db.add_all([debit, credit])

        db.commit()

        return payment

    except Exception as e:
        db.rollback()

        raise e
