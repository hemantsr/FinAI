import yfinance as yf

def fetch_prices(symbol, period="1y"):
    try:
        ticker = yf.Ticker(symbol + ".NS")
        df = ticker.history(period=period)

        if df is None or df.empty:
            return None

        return df

    except Exception as e:
        return None

