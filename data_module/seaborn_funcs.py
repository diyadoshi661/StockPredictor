# Imports for graphing
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Imports for data
import yfinance as yf

def prediction_graph(ticker):
    """Creates a graph of the actual and predicted trend for the given ticker"""
    img = io.BytesIO()

    # Plot actual trend
    apple_data = yf.download('AAPL', start='2010-01-01')
    apple_df = apple_data.reset_index()
    apple_df['Days'] = (apple_df['Date'] - apple_df['Date'].min()).dt.days # Convert date to days
    plt.plot(apple_df["Days"], apple_df["Close"])

    # Plot predicted trend
    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    prediction_plot = base64.b64encode(img.getvalue()).decode('utf8')
    return prediction_plot