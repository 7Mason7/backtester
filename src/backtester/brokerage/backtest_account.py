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

    def get_cash_available_to_invest(self, price_dict: Dict[str, float]) -> float:
        """
        Gets the total cash available including open orders(cash - open orders)
        """
        return self.cash - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: Dict[str, float]) -> float:
        """
        Gets the total open order cost within the OMS.
        """
        order_cost = 0
        for order in self.oms.open_orders.values():
            if order.direction == "buy":
                if isinstance(order, MarketOrder):
                    order_cost += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    order_cost += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    order_cost += order.quantity * order.stop_price
                else:
                    order_cost += order.quantity * price_dict[order.symbol]
        return order_cost


class BacktestMarginAccount(Account):
    """
    Work in progress

    A basic margin account for backtesting. Supported order types are Market, Limit, and Stop.
    """
    def __init__(self):
        super().__init__()
        self.oms = OMS()
        self.margin_balance: float = 0
    
    def get_cash_available_to_invest(self, price_dict: Dict[str, float]) -> float:
        """
        Gets total cash including open orders (cash +/- margin - open orders)
        """
        return self.cash + self.margin_balance - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: Dict[str, float]) -> float:
        """
        Gets the total open order cost within the OMS.
        """
        order_cost = 0
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
        return order_cost

    def get_buying_power(self, price_dict: Dict[str : float]) -> float:
        order_req = 0
        for order in self.oms.open_orders.values():
            if order.direction == "buy":
                if isinstance(order, MarketOrder):
                    order_req += 0.25 * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += 0.25 * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += 0.25 * order.stop_price * order.quantity
            elif order.direction == "sell" and order.short == True:
                if isinstance(order, MarketOrder):
                    order_req += 0.30 * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += 0.30 * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += 0.30 * order.stop_price * order.quantity
        return self.get_equity(price_dict) - order_req

    def get_equity(self, price_dict: Dict[str : float]) -> float:
        equity = self.cash + self.margin_balance
        for symbol in self.holdings:
            equity += self.holdings[symbol] * price_dict[symbol]
        return equity
    
    def get_maintenance_requirement(self):
        

        
