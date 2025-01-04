import datetime
from flask import Flask, request, make_response
from strategies.dmi import calcDMI
from strategies.cci import calcCCI
from strategies.cmo import calcCMO
from strategies.rsi import calcRSI
from strategies.stochastic import calcSO
from strategies.moving_averages import moving_avg_crossover_strategy

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def get_image():
    issuer = request.json.get('issuer', 'ALK')
    interval = request.json.get('interval', '180')
    prikaz = request.json.get('prikaz', 'SMA')

    today = datetime.date.today()
    last = today - datetime.timedelta(days=int(interval))

    intervals = {
        '7': (2, 4),
        '14': (3, 7),
        '30': (5, 10),
        '60': (10, 20),
        '90': (15, 30),
        '120': (20, 40),
        '180': (30, 60)
    }

    short_window, long_window = intervals.get(interval, (2, 4))

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
