from .order import *
import numbers

def check_order_fill(self, price: float, order: Order) -> bool:
    """
    Pass a price and order to check if it is due for a fill. Supports MarketOrder, LimitOrder, and StopOrder
    """
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