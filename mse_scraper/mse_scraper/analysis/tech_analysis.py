import datetime
from flask import Flask, request, make_response
from oscilators.dmi import calcDMI
from oscilators.cci import calcCCI
from oscilators.cmo import calcCMO
from oscilators.rsi import calcRSI
from oscilators.stochastic import calcSO
from moving_averages import moving_avg_crossover_strategy

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def get_image():
    issuer = request.json.get('issuer', 'ALK')
    interval = request.json.get('interval', '7')
    prikaz = request.json.get('prikaz', 'SMA')

    today = datetime.date.today()
    last = today - datetime.timedelta(days=int(interval))

    if interval == '7':
        short_window = 2
        long_window = 4
    elif interval == '14':
        short_window = 3
        long_window = 7
    elif interval == '30':
        short_window = 5
        long_window = 10
    elif interval == '60':
        short_window = 10
        long_window = 20
    elif interval == '90':
        short_window = 15
        long_window = 30
    elif interval == '120':
        short_window = 20
        long_window = 40
    elif interval == '180':
        short_window = 30
        long_window = 60
    else:
        short_window = 2
        long_window = 4

    action= ''
    if prikaz == 'DMI':
        results = calcDMI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
        img_io = results[0]
        action = results[1]
    elif prikaz == 'CCI':
        results = calcCCI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
        img_io = results[0]
        action = results[1]
    elif prikaz == 'CMO':
        results = calcCMO(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
        img_io = results[0]
        action = results[1]
    elif prikaz == 'RSI':
        results = calcRSI(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
        img_io = results[0]
        action = results[1]
    elif prikaz == 'SO':
        results = calcSO(issuer=issuer, interval=interval, start_date=last, end_date=today, short_window=short_window)
        img_io = results[0]
        action = results[1]
    else:
        results = moving_avg_crossover_strategy(issuer=issuer, start_date=last, end_date=today, avg_type=prikaz, fast_window=short_window, slow_window=long_window, interval=interval)
        img_io = results[0]
        action = results[1]

    print(action)
    response = make_response(img_io.read())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
