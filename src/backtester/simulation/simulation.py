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

class Simulation:
    def __init__(
        self,
        account: Account,  # Can be either BacktestCashAccount or BacktestMarginAccount
        start_date: pd.Timestamp = None,
        end_date: pd.Timestamp = None
    ):
        self.account = account
        self.start_date = start_date
        self.end_date = end_date
        self.current_time_index = 0
        self.price_dict = {}
        self.performance_history = []
        
    