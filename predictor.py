from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for

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
# TODO: Update secret key and create env file
app.secret_key = '98a01296f190c59a173a988b90148a22ec7c5100589a6faf8b246973b563f577'

# Create all routes
@app.route('/')
def index():
    # Dates that can be picked by user to predict up to
    today = date.today()
    min_date = today + timedelta(days=1)
    max_date = today + timedelta(days=2)

    return render_template('index.html', date=min_date, max_date=max_date, prediction_graph=get_graph_link('AAPL'))

@app.route('/simulation')
def simulation():
    if 'username' in session:
        return render_template('simulation.html', logged_in=True, signup=False)
    return render_template('simulation.html', logged_in=False, signup=False)

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

@app.post('/signup')
def signup():
    username = request.form['username-signup']
    password = request.form['password-signup']
    # Check if username and password are valid
    if len(username) == 0 or len(password) == 0:
        flash('All fields must be filled')
        return render_template('simulation.html', logged_in=False, signup=True)
    conn = get_simulator_db()
    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM Users WHERE username = '{ username }'")
    results = c.fetchall()
    # Invalid username
    if results[0][0] > 0:
        flash("Username is already in use")

    return redirect(url_for('simulation'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404