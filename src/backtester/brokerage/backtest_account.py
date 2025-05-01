from .account import Account
from .order_management_system import OMS
from .order import *

class BacktestCashAccount(Account):
    """
    A basic cash account for backtesting. Supported order types are Market, Limit, and Stop.
    """
    def __init__(self):
        super().__init__()
        self.oms = OMS()

    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Gets the total cash available including open orders(cash - open orders)
        """
        return self.cash - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: dict[str, float]) -> float:
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
    
    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Gets total cash including open orders (cash +/- margin - open orders)
        """
        return self.cash + self.margin_balance - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: dict[str, float]) -> float:
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

    def get_open_order_req(self, price_dict: dict[str : float]) -> float:
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
                    order_req += 0.3 * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += 0.3 * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += 0.3 * order.stop_price * order.quantity
        return order_req

    def get_equity(self, price_dict: dict[str : float]) -> float:
        equity = self.cash + self.margin_balance
        for symbol in self.holdings:
            equity += self.holdings[symbol] * price_dict[symbol]
        return equity

    def get_maintenance_requirement(self, price_dict: dict[str : float]) -> float:
        req = 0
        for symbol in self.holdings:
            if self.holdings[symbol] > 0:
                req += 0.25 * self.holdings[symbol] * price_dict[symbol]
            elif self.holdings[symbol] < 0:
                req += 0.30 * abs(self.holdings[symbol]) * price_dict[symbol]
        return req

    def get_maintenance_excess(self, price_dict: dict[str : float]) -> float:
        return self.get_equity(price_dict) - self.get_maintenance_requirement(price_dict)
    
    def get_buying_power(self, price_dict: dict[str : float], short = False) -> float:
        if short == False:
            return min(self.get_maintenance_excess(price_dict) / 0.25, 0.5 * self.get_equity(price_dict))
        else:
            return min(self.get_maintenance_excess(price_dict) / 0.3, 0.5 * self.get_equity(price_dict))