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

def plot_historical_data(symbol, num_years):
    end_date = pd.to_datetime('today')
    start_date_plotting = end_date - pd.DateOffset(years=num_years)

    historical_data_plotting = yf.download(symbol, start=start_date_plotting, end=end_date, interval='1mo')
    historical_data_plotting.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
    historical_data_plotting.rename(columns={'Adj Close': 'Stock'}, inplace=True)

    # Assuming 'Market' is a DataFrame with a column named 'Market'
    Market = yf.download('SPY', start=start_date_plotting, end=end_date, interval='1mo')
    Market.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
    Market.rename(columns={'Adj Close': 'Market'}, inplace=True)

    merged_data = pd.merge(historical_data_plotting, Market, left_index=True, right_index=True, how='inner')

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data.index, merged_data['Stock'], label=symbol)
    plt.plot(merged_data.index, merged_data['Market'], label='Market')
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price')
    plt.title(f'{symbol} vs Market - Historical Data')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as an image
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_str = base64.b64encode(img_buf.read()).decode('utf-8')
    img_tag = f'<img src="data:image/png;base64,{img_str}" alt="Historical Data Plot">'

    # Return the merged data and the img tag
    return merged_data, img_tag

def analyze_stock_data(symbol, risk_free_rate, num_years):
    num_stocks_bought = 1
    RF = risk_free_rate

    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(years=num_years)

    historical_data = yf.download(symbol, start=start_date, end=end_date, interval='1mo')

    historical_data['Return'] = historical_data['Adj Close'].pct_change()
    historical_data['Return+1'] = 1 + historical_data['Return']
    historical_data['Cum_Return'] = historical_data['Return+1'].cumprod() - 1
    historical_data['Cum_$Return'] = num_stocks_bought * (1 + historical_data['Cum_Return'])

    annual_return = ((1 + historical_data['Return'].mean()) ** 12) - 1

    geometric_monthly = (historical_data['Return+1'][1:].prod()) ** (1 / (historical_data['Return+1'][1:].count())) - 1
    geometric_annually = ((1 + geometric_monthly) ** 12) - 1

    sd_monthly = historical_data['Return'][1:].std(ddof=1)
    sd_annually = sd_monthly * math.sqrt(12)

    sharpe_ratio = (annual_return - RF) / sd_annually

    market_data = yf.download('SPY', start=start_date, end=end_date, interval='1mo', progress=False)[['Adj Close']]

    common_dates = historical_data.index.intersection(market_data.index)
    common_returns_market = market_data.loc[common_dates, 'Adj Close'].pct_change().dropna()
    common_returns_stock = historical_data.loc[common_dates, 'Return'].dropna()
    beta = np.polyfit(common_returns_market, common_returns_stock, 1)[0]

    df = pd.DataFrame({
        'Arithmetic Average - Monthly': [historical_data['Return'].mean()],
        'Arithmetic Return - Annually': [annual_return],
        'Geometric Average - Monthly': [geometric_monthly],
        'Geometric Average - Annually': [geometric_annually],
        'Standard Deviation - Monthly': [sd_monthly],
        'Standard Deviation - Annually': [sd_annually],
        'Sharpe Ratio': [sharpe_ratio],
        'Beta': [beta]
    }, index=[symbol])

    standard_deviation = df['Arithmetic Return - Annually'].mean()
    standard_deviation = pd.DataFrame([standard_deviation], columns=['Expected'], index=[symbol])
    standard_deviation['68_left'] = standard_deviation['Expected'] - (1 * df['Standard Deviation - Annually'])
    standard_deviation['95_left'] = standard_deviation['Expected'] - (2 * df['Standard Deviation - Annually'])
    standard_deviation['97_left'] = standard_deviation['Expected'] - (3 * df['Standard Deviation - Annually'])
    standard_deviation['68_right'] = standard_deviation['Expected'] + (1 * df['Standard Deviation - Annually'])
    standard_deviation['95_right'] = standard_deviation['Expected'] + (2 * df['Standard Deviation - Annually'])
    standard_deviation['97_right'] = standard_deviation['Expected'] + (3 * df['Standard Deviation - Annually'])
    new_order = ['97_left', '95_left', '68_left', 'Expected', '68_right', '95_right', '97_right']
    standard_deviation = standard_deviation[new_order]
    standard_deviation = pd.DataFrame(standard_deviation)

    stock_analysis_df = pd.DataFrame(df)
    standard_deviation_df = pd.DataFrame(standard_deviation)

    stock_analysis_html = stock_analysis_df.to_html(classes='table table-striped table-bordered', escape=False)
    standard_deviation_html = standard_deviation_df.to_html(classes='table table-striped table-bordered', escape=False)

    # Plot historical data
    merged_data, historical_plot_img = plot_historical_data(symbol, num_years)  # You can adjust the number of years as needed

    return stock_analysis_html, standard_deviation_html, historical_plot_img
