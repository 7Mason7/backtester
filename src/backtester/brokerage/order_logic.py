from .order import *
import numbers

def check_order_fill(price: float, order: Order) -> bool:
    """
    Check if an order should be filled at the given price.
    
    Args:
        price: Current market price
        order: Order to check for fill
        
    Returns:
        bool: True if order should be filled, False otherwise
        
    Raises:
        TypeError: If order is not a supported order type
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