import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators.indicators.common import Quote
from stock_indicators import indicators
import io
from sqlalchemy import create_engine

def calcDMI(issuer, interval, start_date, end_date, short_window):
    engine = create_engine(
        "postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse"
    )

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    # df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    # df.set_index('entrydate', inplace=True)
    df = df.tail(pd.to_numeric( interval)+20)

    quotes = [
        Quote(row['entrydate'], None, row['maximumprice'], row['minimumprice'], row['avgprice'], None)
        for _, row in df.iterrows()
        if pd.notnull(row['maximumprice']) and pd.notnull(row['minimumprice']) and pd.notnull(row['avgprice'])
    ]

    results = indicators.get_dema(quotes, lookback_periods=short_window)
    print(results[0].dema)

    dates = [result.date for result in results if result.dema is not None]
    print(dates)
    demarker_values = [result.dema for result in results if result.dema is not None]
    action_var = demarker_values[len(demarker_values) - 1]

    # Step 8: Plot DeMarker Indicator
    plt.figure(figsize=(12, 6))

    # Plot DeMarker values
    plt.plot(dates, demarker_values, label=f"DeMarker ({short_window})", color="black", linewidth=1.5)

    # Add reference lines for 0.7 (overbought) and 0.3 (oversold)
    plt.axhline(y=0.7, color='green', linestyle='--', label="Overbought (0.7)")
    plt.axhline(y=0.3, color='red', linestyle='--', label="Oversold (0.3)")

    # Customize plot
    if action_var is not None:
        if action_var < 0.3:
            action = "BUY"
        elif action_var > 0.7:
            action = "SELL"
        else:
            action = "HOLD"
    else:
        action = "NO DATA"
    plt.text(dates[-1], demarker_values[-1], action, fontsize=12, verticalalignment='bottom', horizontalalignment='right', color='blue')
    plt.title("DeMarker Indicator")
    plt.xlabel("Date")
    plt.ylabel("DeMarker Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()


    return img_io,action