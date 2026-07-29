import secrets

from fastapi import HTTPException, Depends

from src.databases.database import get_db

from src.auth.verify_user import get_current_user

from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError

import hashlib

from src.databases.models import Customer, LinkedBankAccount

from src.schemas.customer import CustomerCreate
from src.schemas.card import CardCreate
from src.schemas.upi_profile import UPIProfileCreate
from src.schemas.link_bank_request import LinkBankRequest
from src.schemas.user import UserCreate
from src.schemas.payment import PaymentCreate


from src.schemas.discover_acccount_req import DiscoverAccountsRequest

from src.security.hash_utils import sha256_hash

from src.services.input_validator import resolve_receiver
from src.services.account_service import get_primary_account

from src.databases.models import (
    Payment,
    Merchant,
    User,
    Account,
    Customer,
    Card,
    UPIProfile,
    LinkedBankAccount,
    LedgerEntry,
)

from src.utils.enums.CardStatus import CardStatus


from src.security.encryption import (
    encrypt_data,
)

from src.utils.card_generator import (
    generate_card_number,
    generate_expiry,
)

from src.security.hash_utils import sha256_hash

from src.schemas.account import AccountCreate

from src.utils.bank_utils import (
    generate_account_number,
    get_ifsc_code,
)


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


def create_user(db: Session, user_data: UserCreate):

    existing = db.query(User).filter(User.mobile_no == user_data.mobile_no).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Mobile number already registered",
        )

    existing_email = db.query(User).filter(User.email == user_data.email).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=user_data.name,
        mobile_no=user_data.mobile_no,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "Your account has been registered sucessfully",
        "user_id": user.id,
        "name": user.name,
        "mobile_no": user.mobile_no,
        "email": user.email,
    }


def get_account_balance(
    db,
    account_id,
):

    account = db.query(Account).filter(Account.id == account_id).first()

    return account


def create_customer(db, customer_data: CustomerCreate):

    aadhar_hash = hashlib.sha256(customer_data.aadhar_no.encode()).hexdigest()

    pan_hash = hashlib.sha256(customer_data.pan_no.encode()).hexdigest()

    aadhar_encrypted = encrypt_data(customer_data.aadhar_no)

    pan_encypted = encrypt_data(customer_data.pan_no)

    customer = Customer(
        full_name=customer_data.full_name,
        dob=customer_data.dob,
        mobile_no=customer_data.mobile_no,
        email=customer_data.email,
        aadhar_hash=aadhar_hash,
        aadhar_encrypted=aadhar_encrypted,
        pan_hash=pan_hash,
        pan_encrypted=pan_encypted,
        address=customer_data.address,
        kyc_verified=True,
    )

    existing_aadhar = (
        db.query(Customer)
        .filter(Customer.aadhar_hash == sha256_hash(customer_data.aadhar_no))
        .first()
    )

    if existing_aadhar:
        raise HTTPException(
            status_code=409,
            detail="Customer with this Aadhar Number already exists...",
        )

    existing_pan = (
        db.query(Customer)
        .filter(Customer.pan_hash == sha256_hash(customer_data.pan_no))
        .first()
    )

    if existing_pan:
        raise HTTPException(
            status_code=409, detail="Customer with this PAN already exists..."
        )

    existing_email = (
        db.query(Customer).filter(Customer.email == customer_data.email).first()
    )

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Customer with this email already exists. Pleas try another email",
        )

    db.add(customer)

    db.commit()
    db.refresh(customer)

    return customer


def create_account(
    db: Session,
    account_data: AccountCreate,
) -> Account:
    customer = (
        db.query(Customer).filter(Customer.id == account_data.customer_id).first()
    )

    if customer is None:

        raise HTTPException(
            status_code=404,
            detail="Customer KYC incomplete",
        )

    account = Account(
        customer_id=customer.id,
        account_number=generate_account_number(),
        bank_name=account_data.bank_name,
        ifsc_code=get_ifsc_code(account_data.bank_name),
        account_type=account_data.account_type,
        balance=account_data.initial_balance,
        status="ACTIVE",
    )

    db.add(account)

    db.commit()
    db.refresh(account)

    return account


def create_card(card_data: CardCreate, db: Session):

    account = db.query(Account).filter(Account.id == card_data.account_id).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    card_no = generate_card_number(
        bank_name=account.bank_name.value,
        network=card_data.network.value,
        account_id=account.id,
    )

    existing_card = (
        db.query(Card)
        .filter(
            Card.account_id == account.id,
            Card.network == card_data.network,
            Card.status == CardStatus.ACTIVE,
        )
        .first()
    )

    if existing_card:
        raise HTTPException(
            status_code=409,
            detail="You already have a active debit card under this account.",
        )

    card_number_hash = sha256_hash(card_no)

    encrypted_card_no = encrypt_data(card_no)

    expiry_month, expiry_year = generate_expiry()

    card = Card(
        account_id=account.id,
        card_number_encrypted=encrypted_card_no,
        last4=card_no[-4:],
        expiry_month=expiry_month,
        expiry_year=expiry_year,
        network=card_data.network,
        card_number_hash=card_number_hash,
    )

    db.add(card)

    db.commit()

    db.refresh(card)

    return {
        "card_id": card.id,
        "card_number": card_no,
        "expiry_month": expiry_month,
        "expiry_year": expiry_year,
        "network": card.network,
    }


def create_upi_profile(
    db: Session,
    profile_data: UPIProfileCreate,
):

    user = db.query(User).filter(User.id == profile_data.user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing = (
        db.query(UPIProfile).filter(UPIProfile.upi_id == profile_data.upi_id).first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="UPI ID already exists. Please login",
        )

    profile = UPIProfile(
        user_id=profile_data.user_id,
        upi_id=profile_data.upi_id,
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile


def fetch_accounts(db: Session, request: DiscoverAccountsRequest):

    user = db.query(User).filter(User.id == request.user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    customer = (
        db.query(Customer).filter(Customer.mobile_no == request.mobile_no).first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="No bank customer found with this mobile number",
        )

    accounts = db.query(Account).filter(Account.customer_id == customer.id).all()

    if not accounts:
        raise HTTPException(
            status_code=404,
            detail="No accounts found",
        )

    return [
        {
            "account_id": account.id,
            "bank_name": account.bank_name,
            "account_type": account.account_type,
        }
        for account in accounts
    ]


def link_bank_acc(
    data: LinkBankRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    profile = (
        db.query(UPIProfile)
        .filter(
            UPIProfile.id == data.upi_profile_id,
            UPIProfile.user_id == current_user.id,
        )
        .first()
    )

    if profile is None:

        raise HTTPException(status_code=404, detail="UPI profile not found")

    card_hash = sha256_hash(data.card_number)

    card = db.query(Card).filter(Card.card_number_hash == card_hash).first()

    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    if card.expiry_month != data.expiry_month or card.expiry_year != data.expiry_year:
        raise HTTPException(status_code=400, detail="Invalid card details")

    # print(card.account)

    account = db.query(Account).filter(Account.id == card.account_id).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    if account.bank_name != data.bank_name:
        raise HTTPException(
            status_code=400,
            detail="Card does not belong to the selected bank",
        )

    existing = (
        db.query(LinkedBankAccount)
        .filter(
            LinkedBankAccount.upi_profile_id == profile.id,
            LinkedBankAccount.account_id == account.id,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=409, detail="Account already linked.")

    has_linked_accounts = (
        db.query(LinkedBankAccount)
        .filter(LinkedBankAccount.upi_profile_id == profile.id)
        .first()
    )

    is_primary = has_linked_accounts is None

    # First linked bank account → create UPI PIN
    if current_user.payment_pin_hash is None:

        if data.pin is None:
            raise HTTPException(
                status_code=400,
                detail="Please create a UPI PIN while linking your bank account",
            )

        current_user.payment_pin_hash = hash_password(data.pin)

    linked_account = LinkedBankAccount(
        upi_profile_id=profile.id,
        account_id=account.id,
        is_primary=is_primary,
    )

    db.add(linked_account)

    db.commit()

    db.refresh(linked_account)

    return {
        "message": "Bank account linked successfully",
        "linked_account_id": linked_account.id,
        "upi_id": profile.upi_id,
        "bank_name": account.bank_name,
        "account_type": account.account_type,
        "is_primary": linked_account.is_primary,
    }


def process_payment_transaction(
    db: Session,
    payment_data: PaymentCreate,
    current_user: User,
):
    # Sender UPI Profile
    sender_profile = (
        db.query(UPIProfile)
        .filter(
            UPIProfile.user_id == current_user.id,
            UPIProfile.is_active == True,
        )
        .first()
    )

    if not sender_profile:
        raise HTTPException(
            status_code=404,
            detail="No active UPI profile found.",
        )

    # Receiver UPI Profile
    receiver_profile = resolve_receiver(
        db,
        payment_data.receiver,
    )

    if receiver_profile.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot transfer money to yourself.",
        )

    sender_account = get_primary_account(db, sender_profile.id)
    receiver_account = get_primary_account(db, receiver_profile.id)

    # Balance Check
    if sender_account.balance < payment_data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance.",
        )

    try:
        # Fraud Detection
        risk_score = 0.0
        fraud_decision = "APPROVED"

        # Example:
        #
        # risk_score = predict_fraud(...)
        #
        # if risk_score > FRAUD_THRESHOLD:
        #     fraud_decision = "BLOCKED"

        # Payment Status
        status = "FAILED" if fraud_decision == "BLOCKED" else "SUCCESS"

        # Create Payment
        payment = Payment(
            sender_upi_profile_id=sender_profile.id,
            receiver_upi_profile_id=receiver_profile.id,
            sender_account_id=sender_account.id,
            receiver_account_id=receiver_account.id,
            transaction_type="P2P",
            amount=payment_data.amount,
            status=status,
            risk_score=risk_score,
            fraud_decision=fraud_decision,
        )

        db.add(payment)
        db.flush()

        # Stop if Fraud Blocked
        if fraud_decision == "BLOCKED":
            db.commit()
            return payment

        # Update Balances
        sender_account.balance -= payment_data.amount
        receiver_account.balance += payment_data.amount

        # Ledger Entries
        debit_entry = LedgerEntry(
            payment_id=payment.id,
            account_id=sender_account.id,
            entry_type="DEBIT",
            amount=payment_data.amount,
        )

        credit_entry = LedgerEntry(
            payment_id=payment.id,
            account_id=receiver_account.id,
            entry_type="CREDIT",
            amount=payment_data.amount,
        )

        db.add(debit_entry)
        db.add(credit_entry)

        db.commit()
        db.refresh(payment)

        return payment

    except SQLAlchemyError:
        db.rollback()
        raise
