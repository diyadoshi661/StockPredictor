from flask import Flask, render_template

# Import custom-made modules
from data_module import *

# Other imports
from datetime import date, timedelta

# Create application
app = Flask(__name__)

@app.route('/')
def index():
    # Dates that can be picked by user to predict up to
    today = date.today()
    max_date = today + timedelta(days=1)

    return render_template('index.html', date=today, max_date=max_date, prediction_plot=prediction_graph("APPL"))

@app.route('/simulation')
def simulation():
    return render_template('simulation.html', date='2018-01-01')