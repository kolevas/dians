from flask import Flask, request, jsonify, make_response
import psycopg2
import pandas as pd
import numpy as np
from keras.src.models import Sequential
from keras.src.layers import LSTM,Dense,Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection to fetch stock data
def fetch_stock_data(issuercode):
    conn = psycopg2.connect(
        database="mse",
        user="mse_owner",
        password="CYXP4fDEiH5g",
        host="ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech",
        port=5432
    )
    query = """
    SELECT entrydate, lasttransactionprice
    FROM issuinghistory
    WHERE issuercode = %s
    ORDER BY entrydate ASC;
    """
    stock_data = pd.read_sql(query, conn, params=(issuercode,))
    conn.close()
    return stock_data

# Prepare data for LSTM
def prepare_data(stock_data):
    stock_data['entrydate'] = pd.to_datetime(stock_data['entrydate'])
    stock_data = stock_data.sort_values('entrydate')

    # Normalize data using MinMaxScaler
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data[['lasttransactionprice']])

    # Create sequences for LSTM
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    seq_length = 30  # Use the last 30 days
    X, y = create_sequences(scaled_data, seq_length)
    X = X.reshape(X.shape[0], X.shape[1], 1)  # Reshape X to be 3D
    return X, y, scaler, stock_data

# Train LSTM model
def train_lstm_model(X_train, y_train, X_val, y_val):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)  # Output layer
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=64, verbose=1)
    return model

# Generate predictions and plot results
def predict_and_plot(issuercode, interval):
    stock_data = fetch_stock_data(issuercode)
    if stock_data.empty:
        return None

    X, y, scaler, stock_data = prepare_data(stock_data)

    split_idx = int(0.7 * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    model = train_lstm_model(X_train, y_train, X_val, y_val)

    y_val_pred = model.predict(X_val)
    y_val_pred = scaler.inverse_transform(y_val_pred)  # Rescale predictions
    y_val_actual = scaler.inverse_transform(y_val.reshape(-1, 1))  # Rescale actual values

    future_predictions = []
    last_sequence = X_val[-1]
    for _ in range(30):  # Predict the next 30 days
        next_pred = model.predict(last_sequence.reshape(1, -1, 1))[0][0]
        future_predictions.append(next_pred)
        last_sequence = np.append(last_sequence[1:], [[next_pred]], axis=0)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()

    last_date = stock_data['entrydate'].iloc[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['entrydate'], stock_data['lasttransactionprice'], label='Historical Prices', color='blue')
    plt.plot(stock_data['entrydate'].iloc[-len(y_val):], y_val_actual, label='Validation Actual', color='green')
    plt.plot(stock_data['entrydate'].iloc[-len(y_val):], y_val_pred, label='Validation Predicted', color='orange')
    plt.plot(future_dates, future_predictions, label='Future Predictions', color='red', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'LSTM Stock Price Prediction for {issuercode}')
    plt.legend()

    # Save the plot to a BytesIO object
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    return img_io

@app.route('/predict', methods=['POST'])
def get_prediction():
    data = request.json
    issuercode = data.get('issuer', 'ALK')
    interval = data.get('interval', '30')

    img_io = predict_and_plot(issuercode, interval)
    if img_io:
        response = make_response(img_io.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return jsonify({'error': 'Data not found for the given issuer'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)