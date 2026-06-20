from fastapi import HTTPException

from src.databases.models import (
    Account,
    LedgerEntry,
    Payment,
)


def process_payment_transaction(
        db,
        payment_data,
        fraud_result,
):
    
    try:
        sender=(
            db.query(Account)
            .filter(Account.id==payment_data["sender_account_id"])
            .with_for_update()
            .first()
            )
    
        receiver=(
                db.query(Account)
                .filter(Account.id==payment_data["receiver_account_id"])
            .with_for_update()
            .first()
            )

        if sender.balance<payment_data["amount"]:
            raise HTTPException(
                400,
                "Insufficient balance",
            )
    
        sender.balance-=payment_data["amount"]

        receiver.balance+=payment_data["amount"]

        payment=Payment(
            merchant_id=payment_data["merchant_id"],
            amount=payment_data["amount"],
            status=fraud_result["decision"],
            risk_score=fraud_result["risk_score"],
            sender_account_id=sender.id,
            receiver_account_id=receiver.id,
        )

        db.add(payment)
        db.flush()


        debit=LedgerEntry(
            payment_id=payment.id,
            account_id=sender.id,
            entry_type="DEBIT",
            amount=payment.amount
        )

        credit=LedgerEntry(
            payment_id=payment.id,
            account_id=receiver.id,
            entry_type="CREDIT",
            amount=payment.amount
        )

        db.add_all([
            debit,
            credit
        ])

        db.commit()
    
        return payment

    except Exception as e:
        db.rollback()

        raise e