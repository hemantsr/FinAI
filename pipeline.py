def normalize_portfolio(df):
    total_value = df["closing_value"].sum()
    portfolio = []

    for _, row in df.iterrows():
        symbol = (
            row["stock_name"]
            .upper()
            .replace("LIMITED", "")
            .replace("LTD.", "")
            .replace("LTD", "")
            .replace(" ", "")
        )

        portfolio.append({
            "stock_name": row["stock_name"],
            "symbol": symbol,
            "isin": row["isin"],
            "allocation_pct": round(row["closing_value"] / total_value * 100, 2)
        })

    return portfolio

def generate_symbol_candidates(stock_name):
    base = (
        stock_name.upper()
        .replace("LIMITED", "")
        .replace("LTD.", "")
        .replace("LTD", "")
        .replace("&", "")
        .strip()
    )

    no_space = base.replace(" ", "")
    spaced = base.replace(" ", "-")

    return list(set([
        no_space,
        spaced,
        base.split()[0]
    ]))
