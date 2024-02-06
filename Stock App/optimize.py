import pandas as pd
import yfinance as yf
import numpy as np
import math
from scipy.optimize import minimize

def calculate_portfolio_metrics(symbols, risk_free_rate, num_years, num_stocks_bought=1):
    def objective(weights, returns, start_date):
        portfolio_return = np.dot(returns.mean(), weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))
        sharpe_ratio = -portfolio_return / portfolio_volatility
        return sharpe_ratio
    
    result_dfs = []  # List to store individual DataFrames

    for symbol in symbols:
        # Download historical data from Yahoo Finance
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.DateOffset(years=num_years)

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
        geometric_monthly = ((1 + historical_data['Return+1']).prod() ** (1 / historical_data['Return+1'].count())) - 1
        geometric_annually = ((1 + geometric_monthly) ** 12) - 1

        # Calculate standard deviations
        sd_monthly = historical_data['Return'][1:].std(ddof=1)
        sd_annually = sd_monthly * math.sqrt(12)

        # Calculate Sharpe Ratio
        sharpe_ratio = (annual_return - risk_free_rate) / sd_annually

        # Calculate Beta
        market_data = yf.download('SPY', start=start_date, end=end_date, interval='1mo', progress=False)[['Adj Close']]  # Replace 'AAPL' with the market symbol

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
            'Weight': [1 / len(symbols)],  # Set weight to 1/n for equal weighting
            'Last Adj Close': [last_adj_close]
        }, index=[symbol])

        result_dfs.append(df)

    # Concatenate the list of DataFrames into a single DataFrame
    final_result_df = pd.concat(result_dfs)

    # Example optimization (you can modify this based on your specific needs)
    returns_df = pd.concat([yf.download(symbol, start=start_date, end=end_date, interval='1mo', progress=False)['Adj Close'].pct_change().dropna() for symbol in symbols], axis=1)
    returns_df.columns = symbols

    bounds = [(0, 1) for _ in range(len(symbols))]
    initial_weights = [1 / len(symbols) for _ in range(len(symbols))]

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1}, {'type': 'ineq', 'fun': lambda w: w})

    result = minimize(objective, initial_weights, args=(returns_df, start_date), bounds=bounds, constraints=constraints, method='SLSQP')

    optimized_weights = result.x

    # Calculate portfolio metrics based on optimized weights
    portfolio_return = np.dot(returns_df.mean(), optimized_weights)
    portfolio_return_ann = ((1 + portfolio_return) ** 12) - 1
    portfolio_volatility = np.sqrt(np.dot(optimized_weights.T, np.dot(returns_df.cov(), optimized_weights)))
    portfolio_volatility_ann = portfolio_volatility * math.sqrt(12)
    portfolio_sharpe_ratio = (portfolio_return_ann - risk_free_rate) / portfolio_volatility_ann

    # Add portfolio metrics to the final_result_df
    portfolio_metrics = pd.DataFrame({
        'Arithmetic Average - Monthly': [portfolio_return],
        'Arithmetic Return - Annually': [portfolio_return_ann],
        'Geometric Average - Monthly': [((1 + returns_df).prod() ** (1 / returns_df.count())).mean() - 1],
        'Geometric Average - Annually': [((1 + returns_df).prod() ** (12 / returns_df.count())).mean() - 1],
        'Standard Deviation - Monthly': [portfolio_volatility],
        'Standard Deviation - Annually': [portfolio_volatility_ann],
        'Sharpe Ratio': [portfolio_sharpe_ratio],
        'Beta': [np.dot(optimized_weights, [df['Beta'].values[0] for df in result_dfs])],
        'Weight': [1],  # Set weight to 1 for the overall portfolio
        'Last Adj Close': [np.nan]  # Set Last Adj Close to NaN for the overall portfolio
    }, index=['Portfolio'])

    final_result_df = pd.concat([final_result_df, portfolio_metrics])  # Concatenate along columns

    # Set the 'Weight' column to NaN for stock rows
    final_result_df.loc[symbols, 'Weight'] = optimized_weights.round(3)
    final_result_df.loc['Portfolio', 'Weight'] = 1

    return final_result_df





