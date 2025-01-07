import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators import indicators
import io
from analysis.utilities.engines import my_engine
from analysis.utilities import quotes


def calcDMI(issuer, interval, short_window=None):
    engine = my_engine()

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(pd.to_numeric( interval)+20)

    results = indicators.get_dema(quotes.get_quotes(df), lookback_periods=short_window)
    print(results[0].dema)

    dates = [result.date for result in results if result.dema is not None]
    print(dates)
    demarker_values = [result.dema for result in results if result.dema is not None]
    action_var = demarker_values[len(demarker_values) - 1]

    plt.figure(figsize=(12, 6))


    plt.plot(dates, demarker_values, label=f"DeMarker ({short_window})", color="black", linewidth=1.5)

    plt.axhline(y=0.7, color='green', linestyle='--', label="Overbought (0.7)")
    plt.axhline(y=0.3, color='red', linestyle='--', label="Oversold (0.3)")


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