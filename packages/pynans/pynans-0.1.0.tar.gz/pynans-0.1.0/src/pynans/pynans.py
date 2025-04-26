import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


class Portfolio:
    def __init__(self, assets):
        self.assets = assets
        self.data = None
        self.returns = None
        self.metrics = {}

    def fetch_data(self, start_date, end_date):
        self.data = yf.download(list(self.assets.keys()),
                                start=start_date,
                                end=end_date)["Close"]
        self.data = self.data.ffill()
        self.returns = self.data.pct_change().dropna()

    def calculate_metrics(self):
        weights = pd.Series(self.assets)
        portfolio_return = (self.returns.mean() * weights).sum() * 252
        portfolio_volatility = (self.returns.cov().dot(weights).dot(weights)) ** 0.5 * (252 ** 0.5)
        sharpe_ratio = portfolio_return / portfolio_volatility

        self.metrics = {
            'Annual Return': portfolio_return,
            'Annual Volatility': portfolio_volatility,
            'Sharpe Ratio': sharpe_ratio
        }

    def plot_performance(self):
        if self.data is not None:
            (self.data / self.data.iloc[0] * 100).plot(figsize=(10, 6))
            plt.title("Portfolio Asset Performance")
            plt.ylabel("Normalized Price")
            plt.xlabel("Date")
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
            print("No data to plot. Please fetch data first.")
