from .account import Account
from .order_management_system import OMS
from .order import *
from typing import Dict

class BacktestCashAccount(Account):
    """
    A basic cash account for backtesting. Supported order types are Market, Limit, and Stop.
    """
    def __init__(self):
        super().__init__()
        self.oms = OMS()

    def get_buying_power(self, price_dict: Dict[str, float]) -> float:
        """
        Gets the total purchasing power (cash - open orders)
        """
        return self.cash - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: Dict[str, float]) -> float:
        """
        Gets the total open order cost within the OMS.
        """
        committed_to_open_orders = 0
        for order in self.oms.open_orders.values():
            if order.direction == "buy":
                if isinstance(order, MarketOrder):
                    committed_to_open_orders += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    committed_to_open_orders += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    committed_to_open_orders += order.quantity * order.stop_price
                else:
                    committed_to_open_orders += order.quantity * price_dict[order.symbol]
        return committed_to_open_orders
