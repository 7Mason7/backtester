# common orders

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

class OrderStatus(Enum):
    OPEN = "open"
    EXECUTED = "executed"
    CANCELLED = "canceled"

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class Order:
    symbol: str
    quantity: int
    order_type: OrderType
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.OPEN
    timestamp: datetime = datetime.now()