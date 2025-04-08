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
        total_position_value: float = 0
        for key in self.holdings:
            total_position_value = total_position_value + self.holdings[key] # * fetch_price(key)    
        return total_position_value + self.cash


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


    def order_cancel(self, order_index: int):
        """
        Cancels a given order at the selected index within the open_orders attribute.

        Parameters
        ----------
        order_index : int, required
            The index of hte order within the Account.open_orders list.
        """
        del self.open_orders[order_index]


    def order_check(self, current_price: float):
        """
        Pass a price to check all open_orders for execution. If the order is executed, the order is removed and added to activity.

        Parameters
        ----------
        current_price : float, required
            The price you want to check the order against.
        """
        executed_orders = []
        for order in self.open_orders:
            order.check_fill(current_price)
            if order.status == "Executed":
                executed_orders.append(order)
                if order.buy_or_sell == "Buy":
                    total_cost = order.executed_price * order.quantity
                    self.cash -= total_cost
                    self.activity.append(-total_cost)
                    self.holdings[order.symbol] = self.holdings.get(order.symbol, 0) + order.quantity
                elif order.buy_or_sell == "Sell":
                    total_proceeds = (order.executed_price * order.quantity)
                    self.cash += total_proceeds
                    self.activity.append(total_proceeds)
                    self.holdings[order.symbol] = self.holdings.get(order.symbol, 0) - order.quantity
        for order in executed_orders:
            self.open_orders.remove(order)