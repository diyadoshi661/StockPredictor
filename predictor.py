from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html', date='2018-01-01')