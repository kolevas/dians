import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators.indicators.common import Quote
from stock_indicators import indicators
import io
from sqlalchemy import create_engine

def calcCMO(issuer, interval, start_date, end_date, short_window):

    # Step 1: Read CSV and clean temp_data
    engine = create_engine(
        "postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse"
    )

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(int(interval)+20)
    df.dropna(inplace=True)
    print(df)
    quotes = [
        Quote(row.entrydate, None, row['maximumprice'], row['minimumprice'], row['avgprice'], None)
        for _, row in df.iterrows()
        if pd.notnull(row['maximumprice']) and pd.notnull(row['minimumprice']) and pd.notnull(row['avgprice'])
    ]

    # Step 6: Calculate CMO (Chande Momentum Oscillator)
    results = indicators.get_cmo(quotes, 20)
    for i in range(0, len(results)):
        print(results[i].cmo)
    # Step 7: Extract dates and CMO values for plotting
    dates = [result.date for result in results if result.cmo is not None]
    cmo_values = [result.cmo for result in results if result.cmo is not None]

    # Step 8: Plot CMO
    plt.figure(figsize=(12, 6))
    plt.plot(dates, cmo_values, label="CMO (20)", color="black", linewidth=1.5)

    # Add reference lines for +50 and -50
    plt.axhline(y=50, color='green', linestyle='--', label="Upper Level (+50)")
    plt.axhline(y=-50, color='red', linestyle='--', label="Lower Level (-50)")

    # Customize plot
    action_var = cmo_values[-1] if cmo_values else None

    if action_var is not None:
        if action_var < -50:
            action = "BUY"
        elif action_var > 50:
            action = "SELL"
        else:
            action = "HOLD"
    else:
        action = "NO DATA"
    plt.text(dates[-1], cmo_values[-1], action, fontsize=12, verticalalignment='bottom', horizontalalignment='right',
             color='blue')
    plt.title("Chande Momentum Oscillator (CMO)")
    plt.xlabel("Date")
    plt.ylabel("CMO Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()


    return img_io, action