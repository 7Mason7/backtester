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

    def get_open_orders_by_symbol(self, symbol: str) -> list[Order]:
        try:
            return [order for order in self.open_orders.values() if order.symbol == symbol]
        except AttributeError as e:
            print(f"Error accessing order attributes {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in get_open_orders_by_symbol: {e}")
            return []
    
    def new_open_order(self, order: Order) -> None:
        try:
            if order.order_id in self.open_orders:
                print(f"Order ID {order.order_id} already exists in open orders")
            else:
                self.open_orders[order.order_id] = order
        except Exception as e:
            print(f"Unexpected error in new_order: {e}")
        
    def cancel_order(self, order_id) -> None:
        try:
            if order_id not in self.open_orders:
                print(f"Order ID {order_id} does not exist in open_orders.")
            else:
                self.open_orders[order_id].status = "cancelled"
                self.cancelled_orders[order_id] = self.open_orders[order_id]
                del self.open_orders[order_id]
        except KeyError as e:
            print(f"Key error while cancelling order ID {order_id}: {e}")
        except Exception as e:
            print(f"Unexpected error in cancel_order: {e}")

