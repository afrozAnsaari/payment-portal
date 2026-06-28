import secrets

import hashlib

from src.databases.models import Customer

from src.schemas.customer import CustomerCreate

from src.databases.models import Payment, Merchant, User, Account


from src.security.password import hash_password


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
    user_data,
):
    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=hash_password(user_data["password"]),
    )

    db.add(user)

    db.flush()

    account = Account(
        user_id=user.id,
        balance=user_data["initial_balance"],
    )

    db.add(account)
    db.commit()
    db.refresh(user)

    return user


def get_account_balance(
    db,
    account_id,
):

    account = db.query(Account).filter(Account.id == account_id).first()

    return account


def create_customer(db, customer_data: CustomerCreate):

    aadhaar_hash = hashlib.sha256(customer_data.aadhar_no.encode()).hexdigest()

    pan_hash = hashlib.sha256(customer_data.pan_no.encode()).hexdigest()

    customer = Customer(
        full_name=customer_data.full_name,
        dob=customer_data.dob,
        mobile_no=customer_data.mobile_no,
        email=customer_data.email,
        aadhar_hash=aadhaar_hash,
        pan_hash=pan_hash,
        address=customer_data.address,
    )

    db.add(customer)

    db.commit()
    db.refresh(customer)

    return customer
