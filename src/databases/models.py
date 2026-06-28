from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Date,
)


from sqlalchemy.sql import func
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from src.databases.database import Base


class Card(Base):

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )

    card_number_hash: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    last4: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
    )

    expiry_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expiry_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    network: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    card_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="cards",
    )


class Merchant(Base):

    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    api_key: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    merchant_id = Column(
        Integer,
    )

    transaction_type = Column(
        String,
    )

    amount = Column(
        Float,
    )

    status = Column(
        String,
    )

    risk_score = Column(
        Float,
    )

    fraud_decision = Column(
        String,
    )

    created_at = Column(
        DateTime,
        default=func.now(),
    )

    sender_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
    )

    receiver_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
    )


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
    )

    # account: Mapped["Account"] = relationship(
    #     back_populates="user",
    #     uselist=False,
    # )
    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    payment_pin_hash: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )


class Account(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="accounts",
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    balance: Mapped[float] = mapped_column(
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # user: Mapped["User"] = relationship(
    #     "User",
    #     back_populates="account",
    # )

    cards: Mapped[list["Card"]] = relationship(
        "Card",
        back_populates="account",
    )


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
    )

    entry_type = Column(
        String,
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=func.now(),
    )


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    dob: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    mobile_no: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    aadhar_hash: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    pan_hash: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    kyc_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        back_populates="customer",
    )
