# Backtester

A Python-based backtesting framework for trading strategies.

## Features

- Support for both cash and margin accounts
- Multiple order types (Market, Limit, Stop)
- Realistic order management system
- Historical data simulation capabilities
- Comprehensive test coverage

## Installation

1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/), our package manager:
```bash
pip install uv
```

2. Clone the repository:
```bash
git clone https://github.com/7Mason7/backtester.git
cd backtester
```

3. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies:
```bash
# Install main dependencies
uv pip install .

# Install development dependencies (optional)
uv pip install ".[dev]"
```

## Usage

### Running Tests

To verify everything is working correctly:
```bash
uv run pytest
```

### Basic Example

```python
from backtester.brokerage import BacktestCashAccount
from backtester.brokerage import MarketOrder

# Create a cash account
account = BacktestCashAccount()

# Place a market order
order = MarketOrder(
    order_id="1",
    symbol="AAPL",
    quantity=100,
    direction="buy",
    time_in_force="day"
)
```

## Project Structure

```
backtester/
├── src/
│   └── backtester/
│       ├── brokerage/     # Account and order management
│       │   ├── account.py
│       │   ├── backtest_account.py
│       │   ├── order.py
│       │   ├── order_logic.py
│       │   └── order_management_system.py
│       ├── simulation/    # Historical data and simulation
│       │   ├── historical_data.py
│       │   └── simulation.py
│       └── analysis/      # Analysis tools and utilities
├── tests/                 # Test suite
│   ├── test_account.py
│   ├── test_backtest_cash_account.py
│   ├── test_backtest_margin_account.py
│   ├── test_order_logic.py
│   ├── test_order_management_system.py
│   └── test_simulation.py
├── pyproject.toml        # Project configuration and dependencies
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

