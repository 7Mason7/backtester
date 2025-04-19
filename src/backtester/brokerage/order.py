# common orders

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

__all__ = [
    "OrderStatus",
    "OrderDirection",
    "OrderType",
    "TimeInForce",
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

class TimeInForce(Enum):
    GTC = "gtc"
    DAY = "day"

@dataclass
class Order:
    order_id: str
    symbol: str
    quantity: int
    direction: OrderDirection
    time_in_force: TimeInForce
    status: OrderStatus = OrderStatus.OPEN
    timestamp: datetime = datetime.now()
    executed_price: float = None
    
@dataclass
class MarketOrder(Order):
    def __post_init__(self):
        self.type = OrderType.MARKET

@dataclass
class LimitOrder(Order):
    limit_price: float= None
    def __post_init__(self):
        self.type = OrderType.LIMIT

@dataclass
class StopOrder(Order):
    stop_price: float = None
    def __post_init__(self):
        self.type = OrderType.STOP
