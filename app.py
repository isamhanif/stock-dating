from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

stock_list = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V",
    "UNH", "XOM", "PG", "JNJ", "MA", "HD", "CVX", "ABBV", "LLY", "PEP", "KO", "AVGO",
    "MRK", "COST", "BAC", "PFE", "DIS", "ADBE", "CRM", "TMO", "ABT", "ACN", "DHR",
    "NFLX", "NKE", "TXN", "NEE", "ORCL", "MCD", "WMT", "LIN", "QCOM", "AMAT", "AMD",
    "INTC", "LOW", "UNP", "UPS", "GS", "C", "BA", "GE", "CAT", "IBM", "BLK", "NOW",
    "ISRG", "VRTX", "HON", "LMT", "ZTS", "MDT", "SPGI", "PLD", "ADI", "SYK", "REGN",
    "T", "MO", "DE", "MMC", "CI", "AXP", "ETN", "BDX", "TJX", "GILD", "CB",
    "EL", "HCA", "CSCO", "CL", "ADP", "BKNG", "EW", "SO", "PANW", "PGR", "APD", "ROST",
    "WM", "AON", "SBUX", "SLB", "ICE", "MAR", "MNST", "AZO", "ORLY", "F", "GM", "PYPL",
    "KO", "KR", "DAL", "UAL", "LULU", "TTD", "SHOP", "ROKU", "SNOW", "DDOG", "ZS",
    "DOCU", "TWLO", "OKTA", "BILL", "NET"
]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        start = request.form["start"]
        end   = request.form["end"]

        try:
            df = yf.download(
                stock_list,
                start=start,
                end=end,
                progress=False,
                auto_adjust=True
            )["Close"]
        except Exception as e:
            result = f"Download failed: {e}"
            return render_template("index.html", result=result)

        df = df.dropna(how="all")
        if df.shape[0] < 2:
            result = "No data available for that date range."
        else:
            first = df.iloc[0]
            last  = df.iloc[-1]
            mask  = first.notna() & last.notna()
            first = first[mask]
            last  = last[mask]

            if first.empty:
                result = "No data available for any of the stocks."
            else:
                returns     = (last - first) / first * 100
                best_stock  = returns.idxmax()
                best_return = returns.max()
                result = (
                    f"{best_stock} had the highest return of "
                    f"{best_return:.2f}% from {start} to {end}."
                )

    return render_template("index.html", result=result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

