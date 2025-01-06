import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators import indicators
import io
from analysis.utilities import quotes, engines


def calcSO(issuer, interval, short_window=None):

    engine = engines.my_engine()

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    df = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    df = df.tail(int(interval) + 14)


    results = indicators.get_stoch(quotes.get_quotes(df), lookback_periods=14, signal_periods=3, smooth_periods=3)

    dates = [result.date for result in results if result.k is not None and result.d is not None]
    stoch_k_values = [result.k for result in results if result.k is not None and result.d is not None]
    stoch_d_values = [result.d for result in results if result.d is not None and result.k is not None]

    print(len(dates))
    print(len(stoch_k_values))
    print(len(stoch_d_values))


    plt.figure(figsize=(12, 6))

    plt.plot(dates, stoch_k_values, label="%K (Stochastic)", color="black", linewidth=1.5)
    plt.plot(dates, stoch_d_values, label="%D (Signal)", color="blue", linestyle="--", linewidth=1.5)

    plt.axhline(y=80, color='green', linestyle='--', label="Overbought (80)")
    plt.axhline(y=20, color='red', linestyle='--', label="Oversold (20)")

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