from backtester.brokerage.order import *
from backtester.brokerage.order_logic import check_order_fill

def test_check_buy_marketorder_for_fill():
    # Arrange:
    order = MarketOrder("123", "SPY", 10, "buy", time_in_force="day")
    # Attempt:
    outcome = check_order_fill(10, order)
    # Assert:
    assert outcome == True, "MarketOrder did not return a fill correctly"

def test_check_buy_limitorder_for_fill():
    # Arrange:
    order1 = LimitOrder("123", "SPY", 10, "buy", limit_price = 10.5, time_in_force="gtc")
    order2 = LimitOrder("321", "AAPL", 5, "sell", limit_price=100, time_in_force="gtc")
    # Attempt:
    outcome1 = check_order_fill(10, order1)
    outcome2 = check_order_fill(90, order2)
    # Assert
    assert outcome1 == True, "Buy limit order did not return a fill correctly"
    assert outcome2 == False, "Sell limit order did not return a fill correctly"