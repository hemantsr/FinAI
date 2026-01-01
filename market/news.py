import yfinance as yf

def fetch_news(symbol):
    if not symbol:
        return []

    try:
        ticker = yf.Ticker(symbol + ".NS")
        news = ticker.news or []
    except Exception:
        return []

    cleaned = []

    for n in news[:5]:
        title = (
            n.get("title")
            or n.get("headline")
            or n.get("summary")
        )

        publisher = (
            n.get("publisher")
            or n.get("source")
            or "Unknown"
        )

        if title:
            cleaned.append({
                "title": title,
                "publisher": publisher
            })

    return cleaned[:3]
