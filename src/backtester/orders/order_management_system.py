from .order import *
from typing import Dict

class OMS:
    """
    OMS (Order Management System) is used to track and manage orders.
    """
    def __init__(self):
        self.orders: Dict[str, Order] = {} # All orders by order_id
        self.open_orders: Dict[str, Order] = {} # OPEN orders by by order_id
        self.executed_orders: Dict[str, Order] = {} # EXECUTED orders by order_id
        self.cancelled_orders: Dict[str, Order] = {} # 

    def create_order(self, order: Order):
        if order.status != OrderStatus.OPEN:
            raise ValueError("Only OPEN orders can be created")
        if order.order_id in self.open_orders

    def cancel_order(self, order_index: int):
        order = self.open_orders[order_index]
        del self.open_orders[order_index]
        self.cancelled_orders.append(order)

    def execute_order(self, order_index: int):
        order = self.open_orders[order_index]
        del self.open_orders[order_index]
        self.executed_orders.append(order)