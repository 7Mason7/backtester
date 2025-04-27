# common orders

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

__all__ = [
    "Order",
    "MarketOrder",
    "LimitOrder",
    "StopOrder"
]

@dataclass
class Order:
    order_id: str
    symbol: str
    quantity: int
    direction: str
    time_in_force: str
    status: str = "open"
    timestamp: datetime = datetime.now()
    executed_price: float = None
    def __post_init__(self):
        if self.time_in_force not in ["day", "gtc"]:
            raise ValueError("time_in_force must be 'day' or 'gtc'")
        if self.status not in ["open", "executed", "cancelled"]:
            raise ValueError("status must be either 'open', 'executed', or 'cancelled'")
    
@dataclass
class MarketOrder(Order):
    def __post_init__(self):
        self.type = "market"

@dataclass
class LimitOrder(Order):
    limit_price: float= None
    def __post_init__(self):
        self.type = "limit"

@dataclass
class StopOrder(Order):
    stop_price: float = None
    def __post_init__(self):
        self.type = "stop"
