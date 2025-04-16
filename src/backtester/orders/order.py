# common orders

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

__all__ = [
    "OrderStatus",
    "OrderDirection",
    "OrderType",
    "Order",
    "MarketOrder",
    "LimitOrder",
    "StopOrder"
]

class OrderStatus(Enum):
    OPEN = "open"
    EXECUTED = "executed"
    CANCELLED = "canceled"

class OrderDirection(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

@dataclass
class Order:
"""
A simple Order base class with standard attributes.

Intended for data and does not handle order execution logic.
"""
    symbol: str
    quantity: int
    direction: OrderDirection
    type: OrderType
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.OPEN
    timestamp: datetime = datetime.now()
    time_in_force: str = "GTC"

    def __post_init__(self):
        # LIMIT, STOP, and STOP_LIMIT order must have a price
        if self.order_type in (OrderType.LIMIT, OrderType.STOP) and self.price is None:
            raise ValueError(f"Order type {self.order_type.value} requires a price, but price is None")
        # MARKET orders should not have a price
        if self.order_type == OrderType.MARKET and self.price is not None:
            raise ValueError("Market orders should not have a price set")
    
@dataclass
class MarketOrder(Order):
    pass

@dataclass
class LimitOrder(Order):
    limit_price: float

@dataclass
class StopOrder(Order):
    stop_price: float