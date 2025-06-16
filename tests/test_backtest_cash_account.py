from backtester.brokerage.order import *
from backtester.brokerage.backtest_account import BacktestCashAccount
from backtester.brokerage.order_management_system import OMS

def test_get_cash_available_to_invest():
    # Arrange:
    price_dict = {"SPY":100, "AAPL":90, "XYZ":9}
    acct = BacktestCashAccount()
    acct.set_cash(200)
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(LimitOrder("1521", "AAPL", 2, "buy", "gtc", limit_price=100))
    acct.oms.new_open_order(LimitOrder("5215", "QQQ", 1, "sell", "day", limit_price=100)) # no effect
    acct.oms.new_open_order(StopOrder("1252", "XYZ", 5, "buy", "day", stop_price=10))
    # Attempt:
    buyingpower = acct.get_cash_available_to_invest(price_dict)
    # Assert:
    print(f"cash is {acct.cash}")
    assert buyingpower == -250

if __name__ == "__main__":
    test_get_cash_available_to_invest()