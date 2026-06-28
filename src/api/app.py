from fastapi import FastAPI


from src.databases.database import engine
from src.databases.models import Base

from src.schemas.transaction import Transaction

from src.api.routes import (
    merchants,
    payments,
    users,
    accounts,
    auth,
    pin,
)


from src.api.routes.bank.customers import router as customer_router


from src.services.fraud.predictor import predict_fraud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fraud Prediction API")


app.include_router(customer_router)
app.include_router(payments.router)
app.include_router(merchants.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)
app.include_router(pin.router)


@app.get("/")
def home():

    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict(transaction: Transaction):

    result = predict_fraud(transaction.model_dump())

    return result
