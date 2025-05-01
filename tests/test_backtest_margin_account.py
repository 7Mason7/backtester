from ..src.backtester.brokerage.order import *
from ..src.backtester.brokerage.backtest_account import BacktestMarginAccount

def test_get_cash_available_to_invest():
    # Arrange:
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
    acct = BacktestMarginAccount()
    acct.set_cash(1000)
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(LimitOrder("1521", "AAPL", 2, "buy", "gtc", limit_price=100))
    acct.oms.new_open_order(LimitOrder("5215", "QQQ", 1, "sell", "day", limit_price=100)) # no effect
    acct.oms.new_open_order(StopOrder("1252", "XYZ", 5, "buy", "day", stop_price=10))
    # Attempt:
    cash_avail = acct.get_cash_available_to_invest(price_dict)
    # Assert:
    assert cash_avail == 550

def test_get_open_order_cost():
    # Arrange:
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
    acct = BacktestMarginAccount()
    acct.set_cash(1000)
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(LimitOrder("1521", "AAPL", 2, "buy", "gtc", limit_price=100))
    acct.oms.new_open_order(LimitOrder("5215", "QQQ", 1, "sell", "day", limit_price=100)) # no effect
    acct.oms.new_open_order(StopOrder("1252", "XYZ", 5, "buy", "day", stop_price=10))
    # Attempt:
    cost = acct.get_open_order_cost(price_dict)
    # Assert:
    assert cost == 450


def test_get_equity():
    # Arrange:
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
    acct = BacktestMarginAccount()
    acct.set_cash(1000)
    acct.holdings = {"SPY":10, "AAPL":1}
    # Attempt:
    equity = acct.get_equity(price_dict)
    # Assert:
    assert equity == 2090

def test_get_maintenance_requirement():
    # Arrange:
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
    acct = BacktestMarginAccount()
    acct.set_cash(1000)
    acct.holdings = {"SPY":10, "AAPL":-1}
    print(acct.holdings)
    # Attempt: 
    req = acct.get_maintenance_requirement(price_dict)
    # Assert:
    assert req == 277


def test_get_maintenance_excess():
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}

def test_get_buying_power(): 
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
