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

    conn = get_predictor_db()
    c = conn.cursor()

    # Plot actual trend
    c.execute(f"SELECT days FROM GraphData WHERE ticker = '{ ticker }' AND actual = 't'")
    days = c.fetchall()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND actual = 't'")
    values = c.fetchall()

    plt.plot(days, values)

    # Plot predicted trend
    c.execute(f"SELECT days FROM GraphData WHERE ticker = '{ ticker }' AND actual = 'f'")
    days = c.fetchall()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }' AND actual = 'f'")
    values = c.fetchall()

    plt.plot(days, values)

    conn.close()

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    prediction_plot = base64.b64encode(img.getvalue()).decode('utf8')
    return prediction_plot