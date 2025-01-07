from flask import Flask
from blueprints import lstm_blueprint, tech_analysis_blueprint
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

# Register blueprints
app.register_blueprint(lstm_blueprint, url_prefix='/predict')
app.register_blueprint(tech_analysis_blueprint, url_prefix='/generate')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)