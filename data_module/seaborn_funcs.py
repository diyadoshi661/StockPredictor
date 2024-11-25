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

def stock_graph(ticker):
    """Returns a graph of the actual trend for the given ticker"""
    img = io.BytesIO()

    conn = get_predictor_db()
    c = conn.cursor()

    # Plot stock trend
    c.execute(f"SELECT days FROM GraphData WHERE ticker = '{ ticker }'")
    days = c.fetchall()
    c.execute(f"SELECT value FROM GraphData WHERE ticker = '{ ticker }'")
    values = c.fetchall()

    plt.plot(days, values)

    conn.close()

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    prediction_plot = base64.b64encode(img.getvalue()).decode('utf8')
    return prediction_plot