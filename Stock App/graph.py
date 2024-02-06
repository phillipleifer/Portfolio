import pandas as pd
import yfinance as yf
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from tabulate import tabulate
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

def get_plot_stock_prices(symbol, years_back=5, interval='1mo'):
    # Set start and end dates
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(years=years_back)

    # Download historical data
    historical_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    # Plot the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(historical_data['Close'], label=symbol)
    plt.title(f'{symbol} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Create the 'static/images' directory if it doesn't exist
    img_dir = os.path.join('static', 'images')
    os.makedirs(img_dir, exist_ok=True)

    # Save the plot as an image file
    img_path = os.path.join(img_dir, f'{symbol}_plot.png')
    plt.savefig(img_path, format='png')
    plt.close()  # Close the plot to avoid showing it with plt.show()

    return historical_data, img_path