# class containing the blueprint for a fake brokerage account

import numpy as np
from .Order import Order

class Account:
    """
    The Account class is the a representation of what a typical brokerage account would contain.
    This includes the cash, holdings, open orders, and a log of activity.
    """
    def __init__(self, cash: float = 1000):
        """
        Initializes a new Account instance with starting cash and empty data structures.

        Parameters
        ----------
        cash : float, optional
            The initial cash balance for the account. Defaults to 1000.

        Attributes
        ----------
        cash : float
            The current cash balance in the account.
        holdings : dict
            A dictionary mapping security symbols to their quantities.
        activity : list
            A list recording account activities (e.g., trades, deposits).
        open_orders : list[Order]
            A list of pending Order objects associated with the account.
        buying_power : float
            The available funds for purchasing securities, initialized to the cash amount.
        """
        self.cash: float = cash
        self.holdings: dict = {}
        self.activity: list = []
        self.open_orders: list[Order] = []
        self.buying_power: float = cash


    def get_portfolio_value(self) -> float:
        """
        Fetches the current balance and positions value combined.
        """
        _total_position_value: float = 0
        for key in self.holdings:
            _total_position_value = _total_position_value + self.holdings[key] # * fetch_price(key)    
        return _total_position_value + self.cash


    def order_create(self, order: Order):
        """
        Adds an existing Order object to the Account's open_orders list.

        Parameters
        ----------
        order : Order, required
            An instance of the Order class to be added to open_orders.

        Raises
        ------
        TypeError
            If the provided order is not an instance of the Order class.
        """
        if not isinstance(order, Order):
            raise TypeError("Parameter 'order' must be an instance of Order")
        self.open_orders.append(order)


    def order_cancel(self, order_index):
        """
        Cancels a given order at the selected index within the open_orders attribute.
        """
        del self.open_orders[order_index]


    def order_check(self, current_price):
        """
        Pass a price to check all open_orders for execution. If the order is executed, the order is removed and added to activity.
        """
        i = 0
        while i < len(self.open_orders):
            order = self.open_orders[i]
            order.check_fill(current_price)
            if order.status == "Executed":
                if order.buy_or_sell == "Buy":
                    _total_cost = order.executed_price * order.quantity
                    self.cash = self.cash - _total_cost
                    self.activity.append(-_total_cost)
                    self.holdings[order.symbol] = order.quantity
                elif order.buy_or_sell == "Sell":
                    _total_proceeds = (order.executed_price * order.quantity)
                    self.cash = self.cash + _total_proceeds
                    self.activity.append(_total_proceeds)
                    self.holdings[order.symbol] = -order.quantity
                del self.open_orders[i]
            else:
                i += 1
        else:
            i += 1
