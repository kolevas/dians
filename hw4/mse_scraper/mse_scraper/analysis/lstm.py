from flask import Flask, request, jsonify, make_response
import psycopg2
import pandas as pd
import numpy as np
from keras.src.models import Sequential
from keras.src.layers import LSTM,Dense,Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import  timedelta

app = Flask(__name__)

def fetch_stock_data(issuer_code):
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
    stock_data = pd.read_sql(query, conn, params=(issuer_code,))
    conn.close()
    return stock_data

def prepare_data(stock_data):
    stock_data['entrydate'] = pd.to_datetime(stock_data['entrydate'])
    stock_data = stock_data.sort_values('entrydate')

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data[['lasttransactionprice']])


    def create_sequences(data, seq_len):
        x_data, y_data = [], []
        for i in range(len(data) - seq_len):
            x_data.append(data[i:i + seq_len])
            y_data.append(data[i + seq_len])
        return np.array(x_data), np.array(y_data)

    seq_length = 30 
    x, y = create_sequences(scaled_data, seq_length)
    x = x.reshape(x.shape[0], x.shape[1], 1)
    return x, y, scaler, stock_data

# Train LSTM model
def train_lstm_model(x_train, y_train, x_val, y_val):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)  # Output layer
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=20, batch_size=64, verbose=1)
    return model

def predict_and_plot(issuer_code):
    stock_data = fetch_stock_data(issuer_code)
    if stock_data.empty:
        return None

    x, y, scaler, stock_data = prepare_data(stock_data)

    split_idx = int(0.7 * len(x))
    x_train, x_val = x[:split_idx], x[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    model = train_lstm_model(x_train, y_train, x_val, y_val)

    y_val_pred = model.predict(x_val)
    y_val_pred = scaler.inverse_transform(y_val_pred) 
    y_val_actual = scaler.inverse_transform(y_val.reshape(-1, 1)) 

    future_predictions = []
    last_sequence = x_val[-1]
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
    plt.title(f'LSTM Stock Price Prediction for {issuer_code}')
    plt.legend()

    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    return img_io

@app.route('/predict', methods=['POST'])
def get_prediction():
    data = request.json
    issuer_code = data.get('issuer', 'ALK')
    interval = data.get('interval', '30')

    img_io = predict_and_plot(issuer_code)
    if img_io:
        response = make_response(img_io.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return jsonify({'error': 'Data not found for the given issuer'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)