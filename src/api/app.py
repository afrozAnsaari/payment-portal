from fastapi import FastAPI


from src.databases.database import engine
from src.databases.models import Base

from src.schemas.transaction import Transaction

from src.api.routes import (
    merchants,
    users,
    accounts,
    auth,
)

# from src.api.routes.upi.set_acc_pin import set_pin

from src.api.routes.upi.payments import router as make_payments_router


from src.api.routes.bank.customers import router as customer_router

from src.api.routes.bank.accounts import router as bank_account_router

from src.api.routes.bank.card_issuance import router as card_issuance_router

from src.api.routes.upi.profiles import router as UPI_Route

from src.api.routes.upi.fetch_accounts import router as discover_accounts

from src.api.routes.upi.link_bank import router as link_bank_router

from src.services.fraud.predictor import predict_fraud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fraud Prediction API")

app.include_router(link_bank_router)
app.include_router(discover_accounts)
app.include_router(UPI_Route)
app.include_router(card_issuance_router)
app.include_router(bank_account_router)
app.include_router(customer_router)
app.include_router(make_payments_router)
app.include_router(merchants.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)
# app.include_router(set_pin.router)


@app.get("/")
def home():

    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict(transaction: Transaction):

    result = predict_fraud(transaction.model_dump())

    return result
