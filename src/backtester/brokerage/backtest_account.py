from .account import Account
from .order_management_system import OMS, Order, OrderDirection, OrderType, OrderStatus, StopOrder, MarketOrder, LimitOrder

class BacktestAccount(Account):
    
    def __init__(self):
        self.oms = OMS()

    def get_buying_power(self):
        committed_to_open_orders = 0
            for order_id in self.oms:
                committed_to_open_orders += self.oms.open_orders[order_id]