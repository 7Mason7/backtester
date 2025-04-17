from .order import *
import numbers

class OMS:
    """
    OMS (Order Management System) is used to track and manage orders.
    """
    def __init__(self):
        self.open_orders: list[Order] = []
        self.executed_orders: list[Order] = []
        self.cancelled_orders: list[Order] = []

    def create_order(self, order: Order):
        self.open_orders.append(order)

    def cancel_order(self, order_index: int):
        cancelled_order = self.open_orders[order_index]
        del self.open_orders[order_index]
        self.cancelled_orders.append(cancelled_order)

    def execute_order(self, order_index: int):
        executed_order = self.open_orders[order_index]
        del self.open_orders[order_index]
        self.executed_orders.append(executed_order)

    def check_order_fill(self, price: float, order: Order) -> bool:
        if not isinstance(price, numbers.Number): 
            return False
        
        if isinstance(order, MarketOrder):
            return True
        
        elif isinstance(order, LimitOrder):
            if order.direction == "buy":
                return order.limit_price >= price
            elif order.direction == "sell":
                return order.limit_price <= price
            return False
                
        elif isinstance(order, StopOrder):
            if order.direction == "buy":
                return order.stop_price <= price
            elif order.direction == "sell":
                return order.stop_price >= price
            return False
        else:
            raise TypeError("order is not an instance of MarketOrder, LimitOrder, or StopOrder")