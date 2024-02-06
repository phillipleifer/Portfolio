import pandas as pd
import yfinance as yf
import numpy as np
import math
from scipy.optimize import minimize

def calculate_equal_weights(symbol_list, risk_free_rate, num_years, num_stocks_bought=1):
    result_dfs_equal_weights = []  # List to store individual DataFrames
    symbols_equal_weights = []  # List to store symbols for later use

    for symbol in symbol_list:
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.DateOffset(years=num_years)
        risk_free_rate = risk_free_rate
        
        # Include 'Adj Close' during data retrieval
        historical_data = yf.download(symbol, start=start_date, end=end_date, interval='1mo', progress=False)[['Adj Close']]

        # Calculate monthly return
        historical_data['Return'] = historical_data['Adj Close'].pct_change()

        # Calculate cumulative return and cumulative $ return
        historical_data['Return+1'] = 1 + historical_data['Return']
        historical_data['Cum_Return'] = historical_data['Return+1'].cumprod() - 1
        historical_data['Cum_$Return'] = num_stocks_bought * (1 + historical_data['Cum_Return'])

        # Calculate annual return based on the mean of monthly returns
        annual_return = ((1 + historical_data['Return'].mean()) ** 12) - 1

        # Calculate geometric averages
        geometric_monthly = (historical_data['Return+1'][1:].prod()) ** (1 / (historical_data['Return+1'][1:].count())) - 1
        geometric_annually = ((1 + geometric_monthly) ** 12) - 1

        # Calculate standard deviations
        sd_monthly = historical_data['Return'][1:].std(ddof=1)
        sd_annually = sd_monthly * math.sqrt(12)

        # Calculate Sharpe Ratio
        sharpe_ratio = (annual_return - risk_free_rate) / sd_annually

        # Calculate Beta
        market_data = yf.download('SPY', start=start_date, end=end_date, interval='1mo', progress=False)[['Adj Close']]

        # Calculate Beta with common dates
        common_dates = historical_data.index.intersection(market_data.index)
        common_returns_market = market_data.loc[common_dates, 'Adj Close'].pct_change().dropna()
        common_returns_stock = historical_data.loc[common_dates, 'Return'].dropna()
        beta = np.polyfit(common_returns_market, common_returns_stock, 1)[0]

        # Retrieve last adjusted close price
        last_adj_close = historical_data['Adj Close'].iloc[-1]

        # Create a DataFrame with the calculated values as columns
        df = pd.DataFrame({
            'Arithmetic Average - Monthly': [historical_data['Return'].mean()],
            'Arithmetic Return - Annually': [annual_return],
            'Geometric Average - Monthly': [geometric_monthly],
            'Geometric Average - Annually': [geometric_annually],
            'Standard Deviation - Monthly': [sd_monthly],
            'Standard Deviation - Annually': [sd_annually],
            'Sharpe Ratio': [sharpe_ratio],
            'Beta': [beta],
            'Weight': [1 / len(symbol_list)],  # Set weight to 1/n for equal weighting
            'Last Adj Close': [last_adj_close]
        }, index=[symbol])

        result_dfs_equal_weights.append(df)
        symbols_equal_weights.append(symbol)

    # Concatenate the list of DataFrames into a single DataFrame
    final_result_df_equal_weights = pd.concat(result_dfs_equal_weights)

    # Add weights to each stock row (set to NaN for now)
    weights_equal = [round(1 / len(symbols_equal_weights), 3) for _ in range(len(symbols_equal_weights))]  # Equal weights
    final_result_df_equal_weights['Weight'] = weights_equal

    # Calculate portfolio metrics based on equal weights
    portfolio_metrics_equal_weights = pd.DataFrame({
        'Arithmetic Average - Monthly': [final_result_df_equal_weights['Arithmetic Average - Monthly'].mean()],
        'Arithmetic Return - Annually': [final_result_df_equal_weights['Arithmetic Return - Annually'].mean()],
        'Geometric Average - Monthly': [final_result_df_equal_weights['Geometric Average - Monthly'].mean()],
        'Geometric Average - Annually': [final_result_df_equal_weights['Geometric Average - Annually'].mean()],
        'Standard Deviation - Monthly': [final_result_df_equal_weights['Standard Deviation - Monthly'].mean()],
        'Standard Deviation - Annually': [final_result_df_equal_weights['Standard Deviation - Annually'].mean()],
        'Sharpe Ratio': [final_result_df_equal_weights['Sharpe Ratio'].mean()],
        'Beta': [final_result_df_equal_weights['Beta'].mean()],
        'Weight': [1],  # Set weight to 1 for the overall portfolio
        'Last Adj Close': [np.nan]  # Set Last Adj Close to NaN for the overall portfolio
    }, index=['Portfolio'])

    # Concatenate the overall portfolio metrics to the final_result_df_equal_weights
    final_result_df_equal_weights = pd.concat([final_result_df_equal_weights, portfolio_metrics_equal_weights])

    final_result_df_equal_weights = pd.DataFrame(final_result_df_equal_weights)

    # Convert the DataFrame to an HTML table
    final_result_df_equal_weights_to_html = final_result_df_equal_weights.to_html(classes='table table-striped table-bordered', escape=False)

    return final_result_df_equal_weights
