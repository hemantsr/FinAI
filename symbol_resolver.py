import pandas as pd

class SymbolResolver:
    def __init__(self, symbol_master_path: str):
        df = pd.read_csv(symbol_master_path)

        # Normalize column names
        df.columns = (
            df.columns
            .str.lower()
            .str.strip()
            .str.replace(" ", "_")
        )

        # Required columns
        required = {"symbol", "isin_number", "series"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"Symbol master missing columns: {missing}. "
                f"Found: {list(df.columns)}"
            )

        # Keep only equity symbols
        df = df[df["series"] == "EQ"]

        # Clean values
        df["isin_number"] = df["isin_number"].astype(str).str.strip()
        df["symbol"] = df["symbol"].astype(str).str.strip()

        # ISIN → SYMBOL map
        self.isin_map = dict(
            zip(df["isin_number"], df["symbol"])
        )

    def resolve(self, isin: str):
        if not isin:
            return None
        return self.isin_map.get(isin.strip())

