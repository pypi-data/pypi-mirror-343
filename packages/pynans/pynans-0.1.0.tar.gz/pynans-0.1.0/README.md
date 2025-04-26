# Investment Library for Python

A simple and flexible Python library for building, analyzing, and managing investment portfolios. Designed for ease of use by financial analysts, researchers, and individual investors.

## Features

- Portfolio construction and optimization
- Asset performance tracking
- Risk and return analysis
- Visualization tools for financial data
- Support for custom strategies and backtesting

## Installation

```bash
pip install pynans
```

## Quick Start

```python
from pynance import Portfolio

# Create a portfolio with assets
portfolio = Portfolio(assets={
    'AAPL': 0.4,
    'MSFT': 0.3,
    'GOOGL': 0.3
})

# Fetch performance data and analyze
portfolio.fetch_data(start_date="2020-01-01", end_date="2023-01-01")
portfolio.calculate_metrics()
portfolio.plot_performance()
```

## Documentation

Full documentation is available at: [Pynans Docs](https://pynans.readthedocs.io/en/latest/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

Happy Investing! 🌊
