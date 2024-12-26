import pandas as pd
from stock_indicators.indicators.common import Quote
from stock_indicators import indicators
import matplotlib.pyplot as plt
import io
from sqlalchemy import create_engine

def calcCCI(issuer, interval, start_date, end_date, short_window):

    # Step 1: Read CSV and clean temp_data
    engine = create_engine(
        "postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse"
    )

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df=df.tail(int(interval)+20)

    quotes = [
    Quote(row.entrydate, None, row['maximumprice'], row['minimumprice'], row['avgprice'], None)
    for _, row in df.iterrows()
    if pd.notnull(row['maximumprice']) and pd.notnull(row['minimumprice']) and pd.notnull(row['avgprice'])
    ]

    # Step 6: Calculate CCI
    results = indicators.get_cci(quotes, 20)

    # Step 7: Print results
    dates = [result.date for result in results if result.cci is not None]
    cci_values = [result.cci for result in results if result.cci is not None]

    # Step 8: Plot CCI
    plt.figure(figsize=(12, 6))
    plt.plot(dates, cci_values, label=f"CCI ({interval})", color="black", linewidth=1.5)

    # Add reference lines for +100 and -100
    plt.axhline(y=100, color='green', linestyle='--', label="Overbought (+100)")
    plt.axhline(y=-100, color='red', linestyle='--', label="Oversold (-100)")

    # Customize plot
    plt.title("Commodity Channel Index (CCI)")
    plt.xlabel("Date")
    plt.ylabel("CCI Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    return img_io