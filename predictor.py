from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for

# Import custom-made modules
from data_module import *

# Other imports
from datetime import date, datetime, timedelta

def get_graph_link(ticker):
    """Fetches link to prediction graph for specified ticker from database"""
    val = stock_graph(ticker)
    return val

# Create application
app = Flask(__name__)
# TODO: Update secret key and create env file
app.secret_key = '98a01296f190c59a173a988b90148a22ec7c5100589a6faf8b246973b563f577'

# Create all routes
@app.route('/')
def index():
    # Display loading page and update database on load
    return render_template('loading.html')

@app.route('/home')
def home():
    # Display stock prediction values
    conn = get_predictor_db()
    c = conn.cursor()
    c.execute("SELECT value FROM GraphPrediction WHERE ticker = 'AAPL'")
    results = c.fetchall()
    predicted_price = results[0][0]
    # Render final page
    print("rendering...")
    return render_template('index.html', prediction_graph=get_graph_link('AAPL'), predicted_price=predicted_price)

def update_database():
    # Check if database is updated
    conn = get_predictor_db()
    c = conn.cursor()
    c.execute("SELECT MAX(time) FROM GraphPrediction")
    results = c.fetchall()
    if results[0][0] == None:
        print("on no data: updating...")
        update_database()
    last_updated = datetime.strptime(results[0][0], "%Y-%m-%d %H:%M:%S").date() + timedelta(days=-1)
    today = date.today()
    if last_updated < today:
        print("on outdated: updating...")
        update_database()
    conn.close()

# Create post methods
@app.post('/change-graph')
def change_graph():
    try:
        ticker = request.get_json(force=True).get('ticker')
        prediction_graph = get_graph_link(ticker)
    except Exception as ex:
        print(ex)
    finally:
        return jsonify(prediction_graph)

@app.post('/get-predicted-price')
def get_predicted_price():
    try:
        ticker = request.get_json(force=True).get('ticker')
        conn = get_predictor_db()
        c = conn.cursor()
        c.execute(f"SELECT value FROM GraphPrediction WHERE ticker = '{ ticker }'")
        results = c.fetchall()
        price = float(results[0][0])
    except Exception as ex:
        print(ex)
    finally:
        conn.close()
        return jsonify(price)
    
@app.route('/simulation')
def simulation():
    if 'username' in session:
        # Fetch user's assets and history
        conn = get_simulator_db()
        c = conn.cursor()
        c.execute(f"SELECT balance FROM Users where username = '{ session['username'] }'")
        results = c.fetchall()
        balance = '%.2f' % results[0][0]
        c.execute(f"SELECT stock_symbol, quantity_owned FROM Portfolio WHERE username = '{ session['username'] }'")
        assets = c.fetchall()
        c.execute(f"SELECT stock_symbol, action, quantity, price, time FROM Transactions WHERE username = '{ session['username'] }'")
        history = c.fetchall()
        conn.close()
        # Fetch initial price
        conn = get_predictor_db()
        c = conn.cursor()
        c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ 'AAPL' }' AND date = (SELECT MAX(date) FROM GraphData)")
        results = c.fetchall()
        price = float(results[0][0])
        conn.close()
        return render_template('simulation.html', username=session['username'], balance=balance, assets=assets, history=history, price=price)
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    # If user is trying to login
    if request.method == "POST":
        username = request.form.get('username-login')
        password = request.form.get('password-login')
        # Check if username is valid
        conn = get_simulator_db()
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM Users WHERE username = '{ username }'")
        results = c.fetchall()
        if results[0][0] != 1:
            flash("Invalid username")
            conn.close()
            return redirect(url_for('login'))
        # Check if password is correct
        c.execute(f"SELECT password FROM Users WHERE username = '{ username }'")
        results = c.fetchall()
        if results[0][0] != password:
            flash("Incorrect password")
            conn.close()
            return redirect(url_for('login'))
        # Login if everything is correct
        session['username'] = username
        conn.close()   
        return redirect(url_for('simulation'))
    # If user is already logged in 
    if 'username' in session:
        return redirect(url_for('simulation'))
    return render_template('login.html', signup=False)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    # If user is trying to signup
    if request.method == "POST":
        username = request.form['username-signup']
        password = request.form['password-signup']
        password_again = request.form['password-again']
        # Check if username and password are valid
        if len(username) == 0 or len(password) == 0 or len(password_again) == 0:
            flash('All fields must be filled')
            return redirect(url_for('signup'))
        conn = get_simulator_db()
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM Users WHERE username = '{ username }'")
        results = c.fetchall()
        # Invalid username
        if results[0][0] > 0:
            flash("Username is already in use")
            return redirect(url_for('signup'))
        # Invalid password
        if password != password_again:
            flash("Password does not match")
            return redirect(url_for('signup'))
        # If everything is OK, create new user
        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", tuple([username, password]))
        conn.commit()
        conn.close()
        # Login to new user's profile
        session['username'] = username
        return redirect(url_for('simulation'))
    return render_template('login.html', signup=True)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/home')

@app.post('/buy')
def buy():
    # Get ticker
    ticker = request.form.get('ticker')
    # Get quantity
    quantity = float(request.form.get('quantity'))
    # Get price
    conn = get_predictor_db()
    c = conn.cursor()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND date = (SELECT MAX(date) FROM GraphData)")
    results = c.fetchall()
    price = float(results[0][0])
    conn.close()
    # Get total cost
    total_cost = quantity * price
    # Check if user has enough money
    conn = get_simulator_db()
    c = conn.cursor()
    c.execute(f"SELECT balance from Users WHERE username = '{ session['username'] }'")
    results = c.fetchall()
    balance = results[0][0]
    if balance < total_cost:
        flash('Insufficient funds')
        conn.close()
        return redirect(url_for('simulation'))
    # Create recent transaction
    c.execute("INSERT INTO Transactions (username, stock_symbol, action, quantity, price) VALUES (?, ?, ?, ?, ?)", tuple([session['username'], ticker, 'Bought', quantity, price]))
    # Remove previous transaction if exceeding ten
    c.execute(f"SELECT COUNT(*) FROM Transactions WHERE username = '{ session['username'] }'")
    results = c.fetchall()
    if results[0][0] > 10:
        c.execute(f"DELETE FROM Transactions WHERE username = '{ session['username'] }' AND time = (SELECT MIN(time) FROM Transactions)")
    # Add to portfolio
    c.execute(f"UPDATE Portfolio SET quantity_owned = quantity_owned + { quantity } WHERE username = '{ session['username'] }' AND stock_symbol = '{ ticker }'")
    # Update balance
    c.execute(f"UPDATE Users SET balance = balance - { total_cost } WHERE username = '{ session['username'] }'")
    conn.commit()
    conn.close()
    return redirect(url_for('simulation'))

@app.post('/sell')
def sell():
    # Get ticker
    ticker = request.form.get('ticker')
    # Get quantity
    quantity = float(request.form.get('quantity'))
    # Get price
    conn = get_predictor_db()
    c = conn.cursor()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND date = (SELECT MAX(date) FROM GraphData)")
    results = c.fetchall()
    price = float(results[0][0])
    conn.close()
    # Get total profit
    total_profit = quantity * price
    # Check if user has enough stocks
    conn = get_simulator_db()
    c = conn.cursor()
    c.execute(f"SELECT quantity_owned from Portfolio WHERE username = '{ session['username'] }' AND stock_symbol = '{ ticker }'")
    results = c.fetchall()
    quantity_owned = results[0][0]
    if quantity_owned < quantity:
        flash('Insufficient stocks')
        conn.close()
        return redirect(url_for('simulation'))
    # Create recent transaction
    c.execute("INSERT INTO Transactions (username, stock_symbol, action, quantity, price) VALUES (?, ?, ?, ?, ?)", tuple([session['username'], ticker, 'Sold', quantity, price]))
    # Remove previous transaction if exceeding ten
    c.execute(f"SELECT COUNT(*) FROM Transactions WHERE username = '{ session['username'] }'")
    results = c.fetchall()
    if results[0][0] > 10:
        c.execute(f"DELETE FROM Transactions WHERE username = '{ session['username'] }' AND time = (SELECT MIN(time) FROM Transactions)")
    # Add to portfolio
    c.execute(f"UPDATE Portfolio SET quantity_owned = quantity_owned - { quantity } WHERE username = '{ session['username'] }' AND stock_symbol = '{ ticker }'")
    # Update balance
    c.execute(f"UPDATE Users SET balance = balance + { total_profit } WHERE username = '{ session['username'] }'")
    conn.commit()
    conn.close()
    return redirect(url_for('simulation'))

@app.post('/get-price')
def get_price():
    try:
        ticker = request.get_json(force=True).get('ticker')
        conn = get_predictor_db()
        c = conn.cursor()
        c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND date = (SELECT MAX(date) FROM GraphData)")
        results = c.fetchall()
        price = float(results[0][0])
    except Exception as ex:
        print(ex)
    finally:
        conn.close()
        return jsonify(price)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404