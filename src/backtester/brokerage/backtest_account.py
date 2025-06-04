from .account import Account
from .order_management_system import OMS
from .order import *

class BacktestCashAccount(Account):
    """
    A basic cash account for backtesting. Supported order types are Market, Limit, and Stop.

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities.
    activity : list
        A list recording account activities (e.g., trades, deposits).
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
            if order.direction == 'buy':
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

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities.
    activity : list
        A list recording account activities (e.g., trades, deposits).
    oms : OMS
        The order management system object. Used to store and manage orders.
    margin_balance : float, default=0
        The total margin balance. May be negative or postitive.
    margin_requirements : dict
        default= {'initial_long' : 0.5, 'initial_short' : 0.5, 'maint_long' : 0.25, 'maint_short' : 0.3}
        The margin requirements used to calculate maintenance excess and other margin figures.
    """
    def __init__(self):
        super().__init__()
        self.oms = OMS()
        self.margin_balance: float = 0
        self.margin_requirements: dict = {
            'initial_long' : 0.5,
            'initial_short' : 0.5,
            'maint_long' : 0.25,
            'maint_short' : 0.3,
        }
    
    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Gets total cash including open orders (cash +/- margin - open orders)
        """
        return self.cash + self.margin_balance - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: dict[str, float]) -> float:
        """
        Gets the total open order cost within the Order Management System (OMS).
        """
        order_cost = 0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy':
                if isinstance(order, MarketOrder):
                    order_cost += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    order_cost += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    order_cost += order.quantity * order.stop_price
                else:
                    order_cost += order.quantity * price_dict[order.symbol]
        return order_cost

    def get_open_order_maint_req(self, price_dict: dict[str : float]) -> float:
        """
        Gets the total open order maintenance requirements within the Order Management System (OMS).
        """
        order_req = 0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy' and order.short == False:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['maint_long'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['maint_long'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['maint_long'] * order.stop_price * order.quantity
            elif order.direction == 'sell' and order.short == True:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['maint_short'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['maint_short'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['maint_short'] * order.stop_price * order.quantity
        return order_req
    
    def get_open_order_initial_req(self, price_dict: dict[str : float]) -> float:
        """
        Gets the total open order initial margin requirements within the Order Management System (OMS).
        """
        order_req = 0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy' and order.short == False:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['initial_long'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['initial_long'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['initial_long'] * order.stop_price * order.quantity
            elif order.direction == 'sell' and order.short == True:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['initial_short'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['initial_short'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['initial_short'] * order.stop_price * order.quantity
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
                req += self.margin_requirements['maint_long'] * self.holdings[symbol] * price_dict[symbol]
            elif self.holdings[symbol] < 0:
                req += self.margin_requirements['maint_short'] * abs(self.holdings[symbol]) * price_dict[symbol]
        return req

    def get_maintenance_excess(self, price_dict: dict[str : float]) -> float:
        """
        Returns the amount of equity above the maintenance requirement. Negative maintenance excess indicates a maintenance call.
        """
        return self.get_equity(price_dict) - self.get_maintenance_requirement(price_dict)
    