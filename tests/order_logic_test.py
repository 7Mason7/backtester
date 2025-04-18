from ..src.backtester.orders import *

def check_marketorder_for_fill():
    order = Order("SPY", 
                  10, 
                  OrderDirection.BUY, 
                  OrderType.MARKET,
                  )