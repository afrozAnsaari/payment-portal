from fastapi import FastAPI


from src.databases.database import engine
from src.databases.models import Base

from src.api.schemas import Transaction
from src.api.routes import merchants
from src.api.routes import payments


from src.services.fraud.predictor import predict_fraud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fraud Prediction API")

app.include_router(payments.router)
app.include_router(merchants.router)


@app.get("/")
def home():

    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict(transaction: Transaction):

    result = predict_fraud(transaction.model_dump())

    return result
