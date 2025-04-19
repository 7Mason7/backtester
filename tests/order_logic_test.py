from ..src.backtester.orders import *

def check_buy_marketorder_for_fill():
    # Arrange:
    order = MarketOrder("123", "SPY", 10, OrderDirection.BUY, OrderType.MARKET,)
    # Attempt:
    outcome = check_order_fill(10, order)
    # Assert:
    assert outcome == True, "MarketOrder did not return a fill correctly"

def check_buy_limitorder_for_fill():
    # Arrange:
    order1 = LimitOrder("123", "SPY", 10, OrderDirection.BUY, OrderType.LIMIT, limit_price = 10.5)
    order2 = LimitOrder("321", "AAPL", 5, OrderDirection.SELL, limit_price=100)
    # Attempt:
    outcome1 = check_order_fill(10, order1)
    outcome2 = check_order_fill(90, order2)
    # Assert
    assert outcome1 == True, "Buy limit order did not return a fill correctly"
    assert outcome2 == False, "Sell limit order did not return a fill correctly"