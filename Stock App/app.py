from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from tabulate import tabulate
from stock_analysis import analyze_stock_data
from portfolio_analysis import calculate_equal_weights
from optimize import calculate_portfolio_metrics
from custom_weights import calculate_custom_weights
from graph import get_plot_stock_prices



app = Flask(__name__)

# Redirect from root to '/home'
@app.route('/')
def root():
    return redirect(url_for('home'))

# Define a new 'home' route
@app.route('/home')
def home():
    return render_template('home.html')

# Define a new 'index' route
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/getting_started')
def getting_started():
    return render_template('getting_started.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        symbol = request.form['stockSymbol']
        risk_free_rate = float(request.form['riskFreeRate'])
        num_years = int(request.form['num_years'])

        # Call your stock analysis function with the entered risk-free rate
        stock_analysis_html, standard_deviation_html, img_tag = analyze_stock_data(symbol, risk_free_rate, num_years)

        return render_template('index.html', stock_analysis_html=stock_analysis_html,
                               standard_deviation_html=standard_deviation_html,
                               stock_symbol=symbol, historical_plot_img=img_tag)

    return render_template('index.html')

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        # Get the portfolio stock symbols and risk-free rate from the form
        portfolio_stock_symbols = request.form.getlist('portfolioStockSymbol')
        risk_free_rate = float(request.form['riskFreeRate'])  # Convert to float
        num_years = int(request.form['num_years'])

        # Call the portfolio calculation function
        portfolio_results = calculate_equal_weights(portfolio_stock_symbols, risk_free_rate=risk_free_rate, num_years=num_years)

        # Convert the result to HTML table (if it's a DataFrame)
        if isinstance(portfolio_results, pd.DataFrame):
            portfolio_results_html = portfolio_results.to_html(classes='table table-striped table-bordered', escape=False)
        else:
            # Handle the case where portfolio_results is not a DataFrame (e.g., error)
            portfolio_results_html = f"Error: {portfolio_results}"

        return render_template('portfolio.html', portfolio_results_html=portfolio_results_html, portfolio_stock_symbols=portfolio_stock_symbols)

    return render_template('portfolio.html')

@app.route('/optimize', methods=['GET', 'POST'])
def optimize():
    if request.method == 'POST':
        # Get the portfolio stock symbols and risk-free rate from the form
        portfolio_stock_symbols = request.form.getlist('portfolioStockSymbol')
        risk_free_rate = float(request.form['riskFreeRate'])  # Convert to float
        num_years = int(request.form['num_years'])

        # Call the correct optimization function
        optimized_results = calculate_portfolio_metrics(portfolio_stock_symbols, risk_free_rate=risk_free_rate, num_years=num_years)

        # Convert the result to HTML table (if it's a DataFrame)
        if isinstance(optimized_results, pd.DataFrame):
            optimized_results_html = optimized_results.to_html(classes='table table-striped table-bordered', escape=False)
        else:
            # Handle the case where optimized_results is not a DataFrame (e.g., error)
            optimized_results_html = f"Error: {optimized_results}"

        return render_template('optimize.html', optimized_results_html=optimized_results_html, portfolio_stock_symbols=portfolio_stock_symbols)

    return render_template('optimize.html')

@app.route('/custom_weights', methods=['GET', 'POST'])
def custom_weights():
    if request.method == 'POST':
        # Get the portfolio stock symbols and risk-free rate from the form
        symbol_list = request.form.getlist('portfolioStockSymbol')
        risk_free_rate = float(request.form['riskFreeRate'])  # Convert to float
        num_years = int(request.form['num_years'])
        custom_weights = [float(weight) for weight in request.form.getlist('custom_weights')]

        # Call your equal weights function with the entered risk-free rate
        custom_results = calculate_custom_weights(symbol_list, risk_free_rate=risk_free_rate, num_years=num_years, custom_weights=custom_weights)

        return render_template('custom.html', custom_results_html=custom_results.to_html(classes='table table-striped table-bordered'), symbol_list=symbol_list)
    return render_template('custom.html')


def format_analysis_results(stock_analysis, standard_deviation):
    # Format the analysis results using tabulate
    formatted_results = f"Stock Analysis Results:\n{tabulate(stock_analysis, tablefmt='html')}"
    formatted_results += f"<br>Standard Deviation Analysis:\n{tabulate(standard_deviation, tablefmt='html')}"
    return formatted_results

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0', extra_files=['./templates/home.html'])
