import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import ta
from ta.trend import WMAIndicator
import warnings
import io

# Ignore warnings for cleaner output
warnings.filterwarnings('ignore')

def compute_vwma(data, window):
    weighted_price = data['average_price'] * data['volume']
    total_volume = data['volume'].rolling(window=window).sum()
    vwma = weighted_price.rolling(window=window).sum() / total_volume
    return vwma

def moving_avg_crossover_strategy(symbol, start_date=datetime.date.today(), end_date=datetime.date.today(),
                                   fast_window=20, slow_window=50, avg_type='SMA'):
    file_path = f"temp_stocks/temp_data/{symbol}.csv"
    stock_data = pd.read_csv(file_path)

    # Preprocess numeric columns
    for col in ['max', 'min', 'average_price']:
        stock_data[col] = stock_data[col].apply(
            lambda x: ''.join([ch if ch not in '.,' else ',' if ch == '.' else '.' for ch in str(x)]) if pd.notnull(x) else ''
        )
        stock_data[col] = stock_data[col].str.replace(',', '').astype(float, errors='coerce')

    stock_data['volume'] = stock_data['volume'].astype(float, errors='coerce')
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], dayfirst=True)
    stock_data.set_index('Date', inplace=True)

    # Filter data within date range
    stock_data = stock_data.loc[start_date:end_date]

    # Define moving average column names
    fast_col = f"{fast_window}_{avg_type}"
    slow_col = f"{slow_window}_{avg_type}"

    # Compute moving averages
    if avg_type == 'SMA':
        stock_data[fast_col] = stock_data['average_price'].rolling(window=fast_window, min_periods=1).mean()
        stock_data[slow_col] = stock_data['average_price'].rolling(window=slow_window, min_periods=1).mean()
    elif avg_type == 'EMA':
        stock_data[fast_col] = stock_data['average_price'].ewm(span=fast_window, adjust=False).mean()
        stock_data[slow_col] = stock_data['average_price'].ewm(span=slow_window, adjust=False).mean()
    elif avg_type == 'WMA':
        fast_wma = WMAIndicator(close=stock_data['average_price'], window=fast_window)
        slow_wma = WMAIndicator(close=stock_data['average_price'], window=slow_window)
        stock_data[fast_col] = fast_wma.wma()
        stock_data[slow_col] = slow_wma.wma()
    elif avg_type == 'SMMA':
        stock_data[fast_col] = ta.trend.sma_indicator(stock_data['average_price'], window=fast_window)
        stock_data[slow_col] = ta.trend.sma_indicator(stock_data['average_price'], window=slow_window)
    elif avg_type == 'VWMA':
        stock_data[fast_col] = compute_vwma(stock_data, fast_window)
        stock_data[slow_col] = compute_vwma(stock_data, slow_window)

    # Generate trading signals
    stock_data['Signal'] = np.where(stock_data[fast_col] > stock_data[slow_col], 1.0, 0.0)
    stock_data['Position'] = stock_data['Signal'].diff()

    # Create plot
    plt.figure(figsize=(20, 10))
    plt.tick_params(axis='both', labelsize=14)
    stock_data['average_price'].plot(color='black', lw=1, label='Average Price')
    stock_data[fast_col].plot(color='black', lw=1, label=fast_col)
    stock_data[slow_col].plot(color='green', lw=1, label=slow_col)

    # Mark buy and sell signals
    plt.plot(stock_data[stock_data['Position'] == 1].index,
             stock_data[fast_col][stock_data['Position'] == 1],
             '^', markersize=15, color='green', alpha=0.7, label='Buy')
    plt.plot(stock_data[stock_data['Position'] == -1].index,
             stock_data[fast_col][stock_data['Position'] == -1],
             'v', markersize=15, color='red', alpha=0.7, label='Sell')

    # Add labels, title, and legend
    plt.ylabel('Price in MKD', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.title(f"{symbol} - {avg_type} Crossover Strategy", fontsize=20)
    plt.legend()

    # Save the plot as an image
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    plt.close()

    return image_buffer
