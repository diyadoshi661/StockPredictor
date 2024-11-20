# Imports for graphing
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Imports for image generation
import io
import base64

# Import database functions
from .database_funcs import *

# Imports for data
import yfinance as yf

def prediction_graph(ticker):
    """Returns a graph of the actual and predicted trend for the given ticker"""
    img = io.BytesIO()

    # Plot actual trend
    conn = get_predictor_db()
    c = conn.cursor()

    c.execute(f"SELECT days FROM GraphData WHERE ticker = '{ ticker }' AND actual = 't'")
    days = c.fetchall()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND actual = 't'")
    values = c.fetchall()

    plt.plot(days, values)

    conn.close()

    # TODO: Plot predicted trend

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    prediction_plot = base64.b64encode(img.getvalue()).decode('utf8')
    return prediction_plot