# common orders

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = [
    "Order",
    "MarketOrder",
    "LimitOrder",
    "StopOrder"
]

@dataclass
class Order:
    """
    Base class for all order types in the trading system.

    This class defines the common attributes and validation logic for all orders.
    It serves as the foundation for specific order types like Market, Limit, and Stop orders.

    Attributes
    ----------
    order_id : str
        Unique identifier for the order.
    symbol : str
        The trading symbol for the security.
    quantity : int
        Number of shares/units to trade.
    direction : str
        Direction of the trade, either 'buy' or 'sell'.
    time_in_force : str
        Order duration, either 'day' or 'gtc' (good till cancelled).
    short : bool, default=False
        Whether this is a short position.
    status : str, default="open"
        Current status of the order: 'open', 'executed', or 'cancelled'.
    timestamp : datetime, default=datetime.now()
        When the order was created.
    executed_price : float, optional
        The price at which the order was executed, if applicable.
    """
    order_id: str
    symbol: str
    quantity: int
    direction: str
    time_in_force: str
    short: bool = False
    status: str = "open"
    timestamp: datetime = datetime.now()
    executed_price: Optional[float] = None

    def __post_init__(self):
        """Validate order parameters after initialization."""
        if self.time_in_force not in ["day", "gtc"]:
            raise ValueError("time_in_force must be 'day' or 'gtc'")
        if self.status not in ["open", "executed", "cancelled"]:
            raise ValueError("status must be either 'open', 'executed', or 'cancelled'")
        if self.direction not in ["buy", "sell"]:
            raise ValueError("direction must be either 'buy' or 'sell'")
    
@dataclass
class MarketOrder(Order):
    """
    A market order that executes at the current market price.

    Market orders are executed immediately at the best available price.
    """
    def __post_init__(self):
        """Initialize market order specific attributes."""
        super().__post_init__()
        self.type = "market"

@dataclass
class LimitOrder(Order):
    """
    A limit order that executes at a specified price or better.

    Attributes
    ----------
    limit_price : float, optional
        The maximum price for a buy order or minimum price for a sell order.
    """
    limit_price: Optional[float] = None

    def __post_init__(self):
        """Initialize limit order specific attributes and validate limit price."""
        super().__post_init__()
        self.type = "limit"
        if self.limit_price is not None and self.limit_price <= 0:
            raise ValueError("limit_price must be positive")

@dataclass
class StopOrder(Order):
    """
    A stop order that becomes a market order when the stop price is reached.

    Attributes
    ----------
    stop_price : float, optional
        The price at which the order becomes a market order.
    """
    stop_price: Optional[float] = None

    def __post_init__(self):
        """Initialize stop order specific attributes and validate stop price."""
        super().__post_init__()
        self.type = "stop"
        if self.stop_price is not None and self.stop_price <= 0:
            raise ValueError("stop_price must be positive")
