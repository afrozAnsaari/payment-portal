import pandas as pd

FEATURE_COLUMNS = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "origBalanceDiff",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

transaction_types = ["CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]


def preprocess_transaction(data):
    df = pd.DataFrame([data])

    # feature engineering

    df["origBalanceDiff"] = df["oldbalanceOrg"] - df["newbalanceOrig"]

    transaction_type = df["type"].iloc[0]
    # transaction encoding
    df.drop(columns=["type"], inplace=True)

    for t in transaction_types:
        df[f"type_{t}"] = int(transaction_type == t)
    if "step" not in df.columns:
        df["step"] = 1

    df = df[FEATURE_COLUMNS]
    return df
