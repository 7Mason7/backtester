# common orders

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

__all__ = [
    "OrderStatus",
    "OrderDirection",
    "OrderType",
    "Order"
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
    STOP_LIMIT = "stop limit"
    
@dataclass
class Order:
    symbol: str
    quantity: int
    order_direction: OrderDirection
    order_type: OrderType
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.OPEN
    timestamp: datetime = datetime.now()

    def __post_init__(self):
        # LIMIT, STOP, and STOP_LIMIT order must have a price
        if self.order_type in (OrderType.LIMIT, OrderType.STOP, OrderType.STOP_LIMIT) and self.price is None:
            raise ValueError(f"Order type {self.order_type.value} requires a price, but price is None")
        # MARKET orders should not have a price
        if self.order_type == OrderType.MARKET and self.price is not None:
            raise ValueError("Market orders should not have a price set")
    