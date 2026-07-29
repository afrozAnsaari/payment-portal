import pandas as pd

from src.utils.feature_columns import FEATURE_COLUMNS


def preprocess_transaction(data: dict) -> pd.DataFrame:
    return pd.DataFrame([data])[FEATURE_COLUMNS]
