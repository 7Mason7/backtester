# class containing the blueprint for a fake brokerage account

import numpy as np

from .Order import Order

class Account:
    """
    The Account class is the a representation of what a typical brokerage account would contain.
    This includes the cash, holdings, open orders, and a log of activity.
    """
    def __init__(self, cash: float = 1000):
        self.cash: float = cash
        self.holdings: dict
        self.activity: list
        self.open_orders: list
        self.buying_power: float = cash


    def get_portfolio_value(self) -> float:
        """
        Fetches the current balance and positions value combined.
        """
        _total_position_value: float = 0

        for key in self.holdings:
            _total_position_value = _total_position_value + self.holdings[key] # * fetch_price(key)
                                                             
        return _total_position_value + self.cash
        

    def order_create(self, symbol, quantity, order_type, time_in_force, price):
        self.open_orders.append(Order(symbol, quantity, order_type, time_in_force, price))

    def order_cancel(self, index):
        del self.open_orders[index]

    def order_execute(self, index):
        del self.open_orders[index]
    
