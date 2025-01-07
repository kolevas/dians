import pandas as pd
from stock_indicators import indicators
import matplotlib.pyplot as plt
import io
from analysis.utilities import my_engine, quotes


def calcCCI(issuer, interval, short_window=None):

    engine = my_engine()

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(int(interval)+20)

    results = indicators.get_cci(quotes.get_quotes(df), 20)

    dates = [result.date for result in results if result.cci is not None]
    cci_values = [result.cci for result in results if result.cci is not None]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, cci_values, label=f"CCI ({interval})", color="black", linewidth=1.5)

    plt.axhline(y=100, color='green', linestyle='--', label="Overbought (+100)")
    plt.axhline(y=-100, color='red', linestyle='--', label="Oversold (-100)")

    action_var = cci_values[-1] if cci_values else None

    if action_var is not None:
        if action_var < -100:
            action = "BUY"
        elif action_var > 100:
            action = "SELL"
        else:
            action = "HOLD"
    else:
        action = "NO DATA"
    plt.text(dates[-1], cci_values[-1], action, fontsize=12, verticalalignment='bottom', horizontalalignment='right',
             color='blue')

    plt.title("Commodity Channel Index (CCI)")
    plt.xlabel("Date")
    plt.ylabel("CCI Value")
    plt.legend()
    plt.tight_layout()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()


    return img_io, action