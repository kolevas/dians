import datetime

from flask import Flask, send_file, jsonify, request, make_response
import polars as pl

from oscilators.dmi import calcDMI
from oscilators.cci import calcCCI
from oscilators.cmo import calcCMO
from oscilators.rsi import calcRSI
from oscilators.stochastic import calcSO
from moving_averages import moving_avg_crossover_strategy
from oscilators import *
app = Flask(__name__)

# @app.route('/get_names', methods=['GET'])
# def get_issuers():
#     df = pl.read_csv('temp_stocks/names.csv')
#     names = df['Names'].to_list()
#     return jsonify(names)

@app.route('/generate', methods=['GET'])
def get_image():

    issuer = request.args.get('issuer', 'ALK')
    interval = request.args.get('interval', '7')
    prikaz = request.args.get('prikaz', 'SMA')

    today = datetime.date.today()
    last = today - datetime.timedelta(days=int(interval))

    if interval == '7':
        short_window=2
        long_window=4
    elif interval == '14':
        short_window=3
        long_window=7
    elif interval == '30':
        short_window=5
        long_window=10
    elif interval == '60':
        short_window=10
        long_window=20
    elif interval == '90':
        short_window=15
        long_window=30
    elif interval == '120':
        short_window=20
        long_window=40
    elif interval == '180':
        short_window=30
        long_window=60
    else:
        short_window=2
        long_window=4

    if prikaz == 'DMI':
        img_io=calcDMI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
    elif prikaz == 'CCI':
        img_io=calcCCI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
    elif prikaz == 'CMO':
        img_io=calcCMO(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
    elif prikaz == 'RSI':
        img_io=calcRSI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
    elif prikaz == 'SO':
        img_io=calcSO(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
    else:
        img_io=moving_avg_crossover_strategy(issuer=issuer, start_date=last, end_date=today, moving_avg=prikaz, short_window=short_window, long_window=long_window)

    response = make_response(img_io.read())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)