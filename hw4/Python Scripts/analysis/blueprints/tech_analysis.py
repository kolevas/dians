from flask import Blueprint, request, make_response, jsonify
from analysis.indicators.dmi import calcDMI
from analysis.indicators.cci import calcCCI
from analysis.indicators.cmo import calcCMO
from analysis.indicators.rsi import calcRSI
from analysis.indicators.stochastic import calcSO
from analysis.strategies.moving_averages import moving_avg_crossover_strategy
import traceback


# Create the Blueprint
tech_analysis_blueprint = Blueprint('tech_analysis', __name__)

# Mapping for interval windows and indicator functions
INTERVALS = {
    '7': (2, 4),
    '14': (3, 7),
    '30': (5, 10),
    '60': (10, 20),
    '90': (15, 30),
    '120': (20, 40),
    '180': (30, 60)
}

INDICATOR_FUNCTIONS = {
    'DMI': calcDMI,
    'CCI': calcCCI,
    'CMO': calcCMO,
    'RSI': calcRSI,
    'SO': calcSO
}


def get_indicator_results(prikaz, issuer, interval, short_window=None, long_window=None):
    """
    Helper function to get results for the specified indicator.
    """
    if prikaz in INDICATOR_FUNCTIONS:
        # Call the appropriate indicator function
        return INDICATOR_FUNCTIONS[prikaz](issuer=issuer, interval=interval, short_window=short_window)
    else:
        # Default to moving average crossover strategy
        return moving_avg_crossover_strategy(
            issuer=issuer, avg_type=prikaz,
            fast_window=short_window, slow_window=long_window, interval=interval
        )

# Route for generating image with indicators
@tech_analysis_blueprint.route('', methods=['POST'])
def generate_image():
    try:
        data = request.json or {}
        issuer = data.get('issuer', 'ALK')
        interval = data.get('interval', '180')
        prikaz = data.get('prikaz', 'SMA')

        if interval not in INTERVALS:
            return jsonify({"error": "Invalid interval"}), 400

        short_window, long_window = INTERVALS[interval]

        results = get_indicator_results(prikaz, issuer, interval, short_window, long_window)
        img_io, action = results

        response = make_response(img_io.read())
        response.headers['Content-Type'] = 'image/png'
        return response

    except Exception as e:
        # Return an error response in case of failure
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
