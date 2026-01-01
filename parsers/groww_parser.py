import pandas as pd
from parsers.base_parser import BrokerParser

class GrowwParser(BrokerParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, skiprows=9)

        df.columns = [
            "stock_name",
            "isin",
            "quantity",
            "avg_buy_price",
            "buy_value",
            "closing_price",
            "closing_value",
            "unrealised_pnl"
        ]

        df = df[df["stock_name"] != "Stock Name"]
        df = df.dropna(subset=["stock_name", "isin"])

        numeric_cols = ["quantity", "closing_value"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df[["stock_name", "isin", "quantity", "closing_value"]].reset_index(drop=True)
