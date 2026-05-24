import pandas as pd
from core.engine.transformer import DataTransformer


def test_basic_transformations():
    df = pd.DataFrame({
        "name": [" alice ", "Bob", ""],
        "amount": ["100", None, "NULL"],
        "date": ["2023-05-22", "2024-01-01", None]
    })

    tr = DataTransformer(date_columns=["date"], numeric_columns=["amount"])

    df = tr.clean_basic_data(df)
    assert df.loc[0, "name"] == "alice"

    df = tr.handle_missing_numeric(df, ["amount"], default_value=0.0)
    assert df["amount"].dtype != object
    assert df[1]["amount"] == 0.0

    df = tr.add_jalali_columns(df, ["date"])
    # rows with dates should have jalali code populated
    assert "date_jalali_date_code" in df.columns
