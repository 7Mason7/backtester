from .order import *
from typing import Dict

class OMS:
    """
    OMS (Order Management System) is used to track and manage orders.
    """
    def __init__(self):
        self.open_orders: Dict[str, Order] = {}
        self.cancelled_orders: Dict[str, Order] = {}
        self.executed_orders: Dict[str, Order] = {}

    def get_open_order_by_symbol(self, symbol: str) -> list:
        orders: list = []
        for order in self.open_orders.values():
            if order.symbol == symbol:
                orders.append(order)
                return orders
            
    def 



