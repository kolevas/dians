import pandas as pd
import matplotlib.pyplot as plt
import ta
from ta.trend import WMAIndicator
import warnings
import io
from mse_scraper.analysis.utilities import enginges

warnings.filterwarnings('ignore')

def compute_vwma(data, window):
    weighted_price = data['avgprice'] * data['quantity']
    total_volume = data['quantity'].rolling(window=window).sum()
    vwma = weighted_price.rolling(window=window).sum() / total_volume
    return vwma

def moving_avg_crossover_strategy(issuer,
                                   fast_window, slow_window, avg_type, interval):
    engine = enginges.my_engine()

    q = f"SELECT * FROM issuinghistory WHERE issuercode = '{issuer}' ORDER BY entrydate"
    stock_data = pd.read_sql_query(q, engine, index_col="idissuinghistory")
    stock_data.set_index('entrydate', inplace=True)

    stock_data = stock_data.tail(pd.to_numeric(interval))
    fast_col = f"{fast_window}_{avg_type}"
    slow_col = f"{slow_window}_{avg_type}"

    if avg_type == 'SMA':
        stock_data[fast_col] = stock_data['avgprice'].rolling(window=fast_window, min_periods=1).mean()
        stock_data[slow_col] = stock_data['avgprice'].rolling(window=slow_window, min_periods=1).mean()
    elif avg_type == 'EMA':
        stock_data[fast_col] = stock_data['avgprice'].ewm(span=fast_window, adjust=False).mean()
        stock_data[slow_col] = stock_data['avgprice'].ewm(span=slow_window, adjust=False).mean()
    elif avg_type == 'WMA':
        fast_wma = WMAIndicator(close=stock_data['avgprice'], window=fast_window)
        slow_wma = WMAIndicator(close=stock_data['avgprice'], window=slow_window)
        stock_data[fast_col] = fast_wma.wma()
        stock_data[slow_col] = slow_wma.wma()
    elif avg_type == 'SMMA':
        stock_data[fast_col] = ta.trend.sma_indicator(stock_data['avgprice'], window=fast_window)
        stock_data[slow_col] = ta.trend.sma_indicator(stock_data['avgprice'], window=slow_window)
    elif avg_type == 'VWMA':
        stock_data[fast_col] = compute_vwma(stock_data, fast_window)
        stock_data[slow_col] = compute_vwma(stock_data, slow_window)


    signal_values = (stock_data[fast_col] > stock_data[slow_col]).astype(float)
    stock_data['Signal'] = signal_values
    stock_data['Position'] = stock_data['Signal'].diff()

    plt.figure(figsize=(20, 10))
    plt.tick_params(axis='both', labelsize=14)
    stock_data['avgprice'].plot(color='black', lw=1, label='Average Price')
    stock_data[fast_col].plot(color='black', lw=1, label=fast_col)
    stock_data[slow_col].plot(color='green', lw=1, label=slow_col)

    plt.plot(stock_data[stock_data['Position'] == 1].index,
             stock_data[fast_col][stock_data['Position'] == 1],
             '^', markersize=15, color='green', alpha=0.7, label='Buy')
    plt.plot(stock_data[stock_data['Position'] == -1].index,
             stock_data[fast_col][stock_data['Position'] == -1],
             'v', markersize=15, color='red', alpha=0.7, label='Sell')

    action = "HOLD"
    if stock_data['Position'].iloc[-1] == 1:
        action = "BUY"
    elif stock_data['Position'].iloc[-1] == -1:
        action = "SELL"

    # plt.text(stock_data.index[-1], stock_data[fast_col].iloc[-1], action,
    #          fontsize=12, verticalalignment='bottom', horizontalalignment='right', color='blue')
    plt.ylabel('Price in MKD', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.title(f"{issuer} - {avg_type} Crossover Strategy", fontsize=20)
    plt.legend()

    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    plt.close()


    return image_buffer, action
