from src.databases.models import Payment


def create_payment(db, payment_data, fraud_result):
    payment = Payment(
        merchant_id=payment_data["merchant_id"],
        transaction_type=payment_data["type"],
        amount=payment_data["amount"],
        status=fraud_result["decision"],
        risk_score=fraud_result["risk_score"],
        fraud_decision=fraud_result["decision"],
    )

    db.add(payment)

    db.commit()

    db.refresh(payment)

    return payment
