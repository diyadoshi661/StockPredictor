from flask import Flask, render_template, request, jsonify

# Import custom-made modules
from data_module import *

# Other imports
from datetime import date, timedelta

def get_graph_link(ticker):
    """Fetches link to prediction graph for specified ticker from database"""
    conn = get_predictor_db()
    c = conn.cursor()
    c.execute(f"SELECT link FROM GraphLink WHERE ticker = '{ ticker }'")
    prediction_graph = c.fetchall()
    conn.close()
    return prediction_graph[0][0]

# Create application
app = Flask(__name__)

# Create all routes
@app.route('/')
def index():
    # Dates that can be picked by user to predict up to
    today = date.today()
    max_date = today + timedelta(days=1)

    return render_template('index.html', date=today, max_date=max_date, prediction_graph=get_graph_link('AAPL'))

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
        prediction_graph = get_graph_link(ticker)
    except Exception as ex:
        print(ex)
    finally:
        return jsonify(prediction_graph)