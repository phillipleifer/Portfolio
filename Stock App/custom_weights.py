import pandas as pd
import numpy as np
import yfinance as yf
import math

def calculate_custom_weights(symbol_list, risk_free_rate, num_years, custom_weights, num_stocks_bought=1):
    result_dfs_custom_weights = []  # List to store individual DataFrames
    symbols_custom_weights = []  # List to store symbols for later use

    for symbol, custom_weight in zip(symbol_list, custom_weights):
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

        # Get the latest closing price
        CLOSE_M = yf.download(symbol, start=start_date, end=end_date, interval='1d')
        CLOSE_M.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
        CLOSE_M.sort_index(inplace=True)
        last_adj_close = CLOSE_M['Adj Close'].iloc[-1]

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
            'Weight': [custom_weight],  # Set weight to the custom weight provided by the user
            'Last Adj Close': [last_adj_close]  # Add the latest closing price
        }, index=[symbol])

        result_dfs_custom_weights.append(df)
        symbols_custom_weights.append(symbol)

    # Concatenate the list of DataFrames into a single DataFrame
    final_result_df_custom_weights = pd.concat(result_dfs_custom_weights)

    # Add weights to each stock row
    weights_custom = [round(weight, 3) for weight in final_result_df_custom_weights['Weight']]
    final_result_df_custom_weights['Weight'] = weights_custom

    # Calculate portfolio metrics based on custom weights
    portfolio_metrics_custom_weights = pd.DataFrame({
        'Arithmetic Average - Monthly': [final_result_df_custom_weights['Arithmetic Average - Monthly'].mean()],
        'Arithmetic Return - Annually': [final_result_df_custom_weights['Arithmetic Return - Annually'].mean()],
        'Geometric Average - Monthly': [final_result_df_custom_weights['Geometric Average - Monthly'].mean()],
        'Geometric Average - Annually': [final_result_df_custom_weights['Geometric Average - Annually'].mean()],
        'Standard Deviation - Monthly': [final_result_df_custom_weights['Standard Deviation - Monthly'].mean()],
        'Standard Deviation - Annually': [final_result_df_custom_weights['Standard Deviation - Annually'].mean()],
        'Sharpe Ratio': [final_result_df_custom_weights['Sharpe Ratio'].mean()],
        'Beta': [final_result_df_custom_weights['Beta'].mean()],
        'Weight': [1],  # Set weight to 1 for the overall portfolio
        'Last Adj Close': [np.nan]  # Set NaN for overall portfolio
    }, index=['Portfolio'])

    # Concatenate the overall portfolio metrics to the final_result_df_custom_weights
    final_result_df_custom_weights = pd.concat([final_result_df_custom_weights, portfolio_metrics_custom_weights])

    final_result_df_custom_weights = pd.DataFrame(final_result_df_custom_weights)

    # Convert the DataFrame to an HTML table
    final_result_df_custom_weights_to_html = final_result_df_custom_weights.to_html(classes='table table-striped table-bordered', escape=False)

    return final_result_df_custom_weights
