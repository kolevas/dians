import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators.indicators.common import Quote
from stock_indicators import indicators
import io
from sqlalchemy import create_engine

def calcRSI(issuer, interval, start_date, end_date, short_window):
    engine = create_engine(
        "postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse"
    )

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(int(interval) + 14)

    quotes = [
        Quote(row.entrydate, None, row['maximumprice'], row['minimumprice'], row['avgprice'], None)
        for _, row in df.iterrows()
        if pd.notnull(row['maximumprice']) and pd.notnull(row['minimumprice']) and pd.notnull(row['avgprice'])
    ]

    # Step 6: Calculate RSI
    results = indicators.get_rsi(quotes, lookback_periods=14)

    # Step 7: Extract dates and RSI values for plotting
    dates = [result.date for result in results if result.rsi is not None]
    rsi_values = [result.rsi for result in results if result.rsi is not None]

    # Step 8: Plot RSI
    plt.figure(figsize=(12, 6))

    # Plot RSI values
    plt.plot(dates, rsi_values, label="RSI (14)", color="black", linewidth=1.5)

    # Add reference lines for 70 and 30
    plt.axhline(y=70, color='green', linestyle='--', label="Overbought (70)")
    plt.axhline(y=30, color='red', linestyle='--', label="Oversold (30)")

    # Customize plot
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