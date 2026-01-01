import numpy as np

def compute_indicators(df):
    # ---- Data validation ----
    if df is None or df.empty or len(df) < 200:
        return {
            "trend": "unknown",
            "dma_alignment": "unknown",
            "rsi_state": "n/a",
            "volatility": "unknown",
            "price_position": "unknown",
            "data_quality": "insufficient"
        }

    df = df.copy()

    # ---- Moving Averages ----
    df["SMA_50"] = df["Close"].rolling(50).mean()
    df["SMA_200"] = df["Close"].rolling(200).mean()

    # ---- RSI (14) ----
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # ---- Volatility (30-day std of returns) ----
    df["returns"] = df["Close"].pct_change()
    volatility = df["returns"].rolling(30).std().iloc[-1]

    # ---- Latest snapshot ----
    latest = df.iloc[-1]

    # ---- Trend logic ----
    if latest["Close"] > latest["SMA_50"] > latest["SMA_200"]:
        trend = "strong_uptrend"
        dma_alignment = "bullish"
    elif latest["Close"] < latest["SMA_50"] < latest["SMA_200"]:
        trend = "strong_downtrend"
        dma_alignment = "bearish"
    else:
        trend = "sideways"
        dma_alignment = "mixed"

    # ---- RSI interpretation ----
    rsi_value = latest["RSI"]
    if rsi_value < 35:
        rsi_state = "oversold"
    elif rsi_value > 70:
        rsi_state = "overbought"
    else:
        rsi_state = "neutral"

    # ---- Volatility bucket ----
    if volatility < 0.015:
        volatility_state = "low"
    elif volatility < 0.03:
        volatility_state = "medium"
    else:
        volatility_state = "high"

    # ---- 52-week position ----
    high_52w = df["Close"].rolling(252).max().iloc[-1]
    low_52w = df["Close"].rolling(252).min().iloc[-1]
    price_position = (latest["Close"] - low_52w) / (high_52w - low_52w)

    if price_position > 0.8:
        price_position_state = "near_52w_high"
    elif price_position < 0.2:
        price_position_state = "near_52w_low"
    else:
        price_position_state = "mid_range"

    return {
        "trend": trend,
        "dma_alignment": dma_alignment,
        "rsi_state": rsi_state,
        "volatility": volatility_state,
        "price_position": price_position_state,
        "data_quality": "good"
    }
