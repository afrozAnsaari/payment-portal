import secrets

from src.databases.models import Payment, Merchant, User, Account


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


def create_merchant(db, merchant_data):

    api_key = "sk_test" + secrets.token_hex(32)

    merchant = Merchant(name=merchant_data["name"], api_key=api_key)

    db.add(merchant)

    db.commit()

    db.refresh(merchant)

    return merchant


def create_user(
    db,
    data,
):
    user = User(
        name=data["name"],
        email=data["email"],
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    account = Account(
        user_id=user.id,
        balance=data["initial_balance"],
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return user


def get_account_balance(
    db,
    account_id,
):

    account = db.query(Account).filter(Account.id == account_id).first()

    return account
