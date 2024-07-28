import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title('Portfolio Analysis Tool')

# Sidebar inputs for user to input their portfolio holdings
st.sidebar.header('Input Portfolio Holdings')

# Example ticker and allocation
example_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
example_allocations = [0.25, 0.25, 0.25, 0.25]

# Input for tickers
tickers = st.sidebar.text_area('Tickers (comma separated)', ', '.join(example_tickers))
tickers = [ticker.strip().upper() for ticker in tickers.split(',')]

# Input for allocations
allocations = st.sidebar.text_area('Allocations (comma separated, in decimals)', ', '.join(map(str, example_allocations)))
allocations = [float(alloc) for alloc in allocations.split(',')]

# Validate the inputs
if len(tickers) != len(allocations):
    st.sidebar.error('The number of tickers must match the number of allocations.')
elif sum(allocations) != 1:
    st.sidebar.error('The sum of the allocations must be 1.')
else:
    # Fetch historical price data
    data = yf.download(tickers, start='2020-01-01')['Adj Close']
    
    if data.isnull().values.any():
        st.error('Some tickers have missing data. Please check the ticker symbols or select a different date range.')
    else:
        # Calculate daily returns
        returns = data.pct_change().dropna()

        # Calculate portfolio returns and volatility
        portfolio_return = np.dot(returns.mean(), allocations) * 252
        portfolio_volatility = np.sqrt(np.dot(allocations, np.dot(returns.cov() * 252, allocations)))
        
        # Risk-free rate (for Sharpe Ratio calculation), assume 2% annual risk-free rate
        risk_free_rate = 0.02
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

        # Display portfolio metrics
        st.header('Portfolio Metrics')
        st.write(f"Expected Annual Return: {portfolio_return:.2%}")
        st.write(f"Annual Volatility: {portfolio_volatility:.2%}")
        st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")

        # Plot portfolio allocation
        st.header('Portfolio Allocation')
        fig, ax = plt.subplots()
        ax.pie(allocations, labels=tickers, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Display historical prices
        st.header('Historical Prices')
        st.line_chart(data)

        # Calculate and display correlation matrix
        st.header('Correlation Matrix')
        correlation_matrix = returns.corr()
        st.write(correlation_matrix)

        # Display pair plots for returns
        st.header('Pair Plot of Returns')
        sns.pairplot(returns)
        st.pyplot(plt)
