from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime


from sqlalchemy.sql import func


from src.databases.database import Base


class Merchant(Base):

    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    api_key = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime, default=func.now())

    is_active = Column(Boolean, default=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    merchant_id = Column(Integer)

    transaction_type = Column(String)

    amount = Column(Float)

    status = Column(String)

    risk_score = Column(Float)

    fraud_decision = Column(String)

    created_at = Column(DateTime, default=func.now())
