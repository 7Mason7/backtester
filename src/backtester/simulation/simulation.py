# Standard library imports
from datetime import datetime
from typing import Dict, Optional

# Third-party imports
import pandas as pd

# Local imports
from src.backtester.brokerage.account import Account
from src.backtester.brokerage.backtest_account import BacktestCashAccount, BacktestMarginAccount
from src.backtester.brokerage.order import Order, MarketOrder, LimitOrder, StopOrder
from src.backtester.brokerage.order_management_system import OMS
from backtester.data.historical_data import HistoricalData

class Simulation:
    def __init__(
        self,
        historical_data: HistoricalData,
        account: Account,  # Can be either BacktestCashAccount or BacktestMarginAccount
        start_date: pd.Timestamp = None,
        end_date: pd.Timestamp = None
    ):
        self.historical_data = historical_data
        self.account = account
        self.start_date = start_date or historical_data.time_index[0]
        self.end_date = end_date or historical_data.time_index[-1]
        self.current_time_index = 0
        self.price_dict = {}
        self.performance_history = []
        
    