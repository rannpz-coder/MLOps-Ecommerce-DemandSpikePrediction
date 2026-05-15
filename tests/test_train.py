import pandas as pd

def test_dataset_not_empty():
    df = pd.read_csv("data/processed/clean_week_03.csv")
    assert len(df) > 0

def test_required_columns():
    df = pd.read_csv("data/processed/clean_week_03.csv")

    required_cols = [
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "StockCode"
    ]

    for col in required_cols:
        assert col in df.columns