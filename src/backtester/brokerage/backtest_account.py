from .account import Account
from ..orders import OMS, check_order_fill, Order, OrderDirection, OrderType, OrderStatus, StopOrder, MarketOrder, LimitOrder

class BacktestAccount(Account):
    
    def __init__(self):
        self.oms = OMS()

    def get_buying_power(self):
        committed_to_open_orders = 0
            for order_id in self.oms:
                committed_to_open_orders += self.oms.open_orders[order_id]