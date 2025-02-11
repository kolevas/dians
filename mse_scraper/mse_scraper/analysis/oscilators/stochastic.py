import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators.indicators.common import Quote
from stock_indicators import indicators
import io
from sqlalchemy import create_engine

def calcSO(issuer, interval, start_date, end_date, short_window):

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

    # Step 6: Calculate Stochastic Oscillator
    results = indicators.get_stoch(quotes, lookback_periods=14, signal_periods=3, smooth_periods=3)

    # Step 7: Extract dates, %K and %D values for plotting
    dates = [result.date for result in results if result.k is not None and result.d is not None]
    stoch_k_values = [result.k for result in results if result.k is not None and result.d is not None]
    stoch_d_values = [result.d for result in results if result.d is not None and result.k is not None]

    print(len(dates))
    print(len(stoch_k_values))
    print(len(stoch_d_values))


    # Step 8: Plot Stochastic Oscillator
    plt.figure(figsize=(12, 6))

    # Plot %K and %D lines
    plt.plot(dates, stoch_k_values, label="%K (Stochastic)", color="black", linewidth=1.5)
    plt.plot(dates, stoch_d_values, label="%D (Signal)", color="blue", linestyle="--", linewidth=1.5)

    # Add reference lines for 80 (overbought) and 20 (oversold)
    plt.axhline(y=80, color='green', linestyle='--', label="Overbought (80)")
    plt.axhline(y=20, color='red', linestyle='--', label="Oversold (20)")

    # Customize plot
    action = "NO DATA"
    if len(stoch_k_values) > 1 and len(stoch_d_values) > 1:
        current_k = stoch_k_values[-1]
        current_d = stoch_d_values[-1]
        previous_k = stoch_k_values[-2]
        previous_d = stoch_d_values[-2]

        if current_k < 20 and current_d < 20 and previous_k < previous_d and current_k > current_d:
            action = "BUY"
        elif current_k > 80 and current_d > 80 and previous_k > previous_d and current_k < current_d:
            action = "SELL"
        else:
            action = "HOLD"
    plt.text(dates[-1], stoch_k_values[-1], action, fontsize=12, verticalalignment='bottom', horizontalalignment='right', color='blue')
    plt.title("Stochastic Oscillator")
    plt.xlabel("Date")
    plt.ylabel("Stochastic Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()


    return img_io, action