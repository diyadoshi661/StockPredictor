from flask import Flask, render_template, request, jsonify

# Import custom-made modules
from data_module import *

# Other imports
from datetime import date, timedelta

# Create application
app = Flask(__name__)

# Create all routes
@app.route('/')
def index():
    # Dates that can be picked by user to predict up to
    today = date.today()
    max_date = today + timedelta(days=1)

    prediction_plot = prediction_graph("AAPL")

    return render_template('index.html', date=today, max_date=max_date, prediction_plot=prediction_plot)

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

# Create post methods
@app.post('/change-graph')
def change_graph():
    # TODO: Fix responses on ticker change
    #       JSON does not always return promise and has thread problems
    try:
        ticker = request.get_json(force=True).get('ticker')
        prediction_plot = prediction_graph(ticker)
    except Exception as ex:
        print(ex)
    finally:
        return jsonify(prediction_plot)