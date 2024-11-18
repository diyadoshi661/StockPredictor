from flask import Flask, render_template
# Imports for graphing
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
# Other imports
from datetime import date, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    # Create seaborn graph
    img = io.BytesIO()
    sns.set_style("dark")

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]

    plt.plot(x,y)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    prediction_plot = base64.b64encode(img.getvalue()).decode('utf8')

    # Dates that can be picked by user to predict up to
    today = date.today()
    max_date = today+timedelta(days=1)

    return render_template('index.html', date=today, max_date=max_date, prediction_plot=prediction_plot)

@app.route('/simulation')
def simulation():
    return render_template('simulation.html', date='2018-01-01')