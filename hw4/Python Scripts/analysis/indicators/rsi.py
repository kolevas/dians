import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators import indicators
import io
from analysis.utilities.engines import my_engine
from analysis.utilities import quotes


def calcRSI(issuer, interval, short_window=None):
    engine = my_engine()

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(int(interval) + 14)

    results = indicators.get_rsi(quotes.get_quotes(df), lookback_periods=14)

    dates = [result.date for result in results if result.rsi is not None]
    rsi_values = [result.rsi for result in results if result.rsi is not None]

    plt.figure(figsize=(12, 6))

    plt.plot(dates, rsi_values, label="RSI (14)", color="black", linewidth=1.5)

    plt.axhline(y=70, color='green', linestyle='--', label="Overbought (70)")
    plt.axhline(y=30, color='red', linestyle='--', label="Oversold (30)")

    action_var = rsi_values[-1] if rsi_values else None

    if action_var is not None:
        if action_var < 30:
            action = "BUY"
        elif action_var > 70:
            action = "SELL"
        else:
            action = "HOLD"
    else:
        action = "NO DATA"
    plt.text(dates[-1], rsi_values[-1], action, fontsize=12, verticalalignment='bottom', horizontalalignment='right',
             color='blue')
    plt.title("Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()


    return img_io, action