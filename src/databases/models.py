from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey


from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from src.databases.database import Base


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

    created_at: Mapped[DateTime] = mapped_column(
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

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=func.now(),
    )

    account = relationship(
        "Account",
        back_populates="user",
        uselist=False,
    )


class Account(Base):

    __tablename__ = "accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
    )

    balance = Column(
        Float,
        default=0,
    )

    created_at = Column(
        DateTime,
        default=func.now(),
    )

    user = relationship(
        "User",
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
