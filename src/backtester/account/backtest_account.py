from .account import Account
from ..orders import *

class BacktestAccount(Account):
    
    def __init__(self):
        self.oms = OMS()

    def get_buying_power(self):
        total_order_cost = 0
        for order in self.oms.open_orders:
            total_order_cost += order.quantity * order.price