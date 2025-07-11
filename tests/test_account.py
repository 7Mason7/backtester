from backtester.brokerage.account import Account, CashAccount, MarginAccount
from backtester.brokerage.order import MarketOrder, LimitOrder, StopOrder

# Base Account Tests
def test_account_deposit_cash():
    # Arrange
    acct = Account()
    # Act
    acct.deposit_cash(100)
    # Assert
    assert acct.cash == 100

def test_account_withdraw_cash():
    # Arrange
    acct = Account()
    # Act
    acct.withdraw_cash(100)
    # Assert
    assert acct.cash == -100

def test_account_get_portfolio_value():
    # Arrange
    acct = Account()
    acct.set_cash(100)
    acct.holdings = {"SPY": 2, "AAPL": 1}
    price_dict = {"SPY": 100, "AAPL": 90}
    # Act
    portfolio_val = acct.get_portfolio_value(price_dict)
    # Assert
    assert portfolio_val == 390  # 100 cash + (2 * 100) + (1 * 90)

def test_account_get_portfolio_value_missing_price():
    # Arrange
    acct = Account()
    acct.holdings = {"SPY": 2}
    price_dict = {}  # Missing SPY price
    # Act & Assert
    try:
        acct.get_portfolio_value(price_dict)
        assert False, "Expected KeyError was not raised"
    except KeyError:
        pass

# Cash Account Tests
def test_cash_account_get_cash_available_to_invest():
    # Arrange
    acct = CashAccount()
    acct.set_cash(1000)
    price_dict = {"SPY": 100, "AAPL": 90}
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(LimitOrder("456", "AAPL", 1, "buy", "gtc", limit_price=100))
    # Act
    available_cash = acct.get_cash_available_to_invest(price_dict)
    # Assert
    assert available_cash == 700  # 1000 - (2 * 100) - (1 * 100)

# Margin Account Tests
def test_margin_account_initialization():
    # Arrange & Act
    acct = MarginAccount()
    # Assert
    assert acct.margin_balance == 0.0
    assert acct.margin_requirements["initial_long"] == 0.5
    assert acct.margin_requirements["initial_short"] == 0.5
    assert acct.margin_requirements["maint_long"] == 0.25
    assert acct.margin_requirements["maint_short"] == 0.3

def test_margin_account_get_cash_available_to_invest():
    # Arrange
    acct = MarginAccount()
    acct.set_cash(1000)
    acct.margin_balance = 500
    price_dict = {"SPY": 100, "AAPL": 90}
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(LimitOrder("456", "AAPL", 1, "buy", "gtc", limit_price=100))
    # Act
    available_cash = acct.get_cash_available_to_invest(price_dict)
    # Assert
    assert available_cash == 1200  # 1000 + 500 - (2 * 100) - (1 * 100)

def test_margin_account_get_equity():
    # Arrange
    acct = MarginAccount()
    acct.set_cash(1000)
    acct.margin_balance = 500
    acct.holdings = {"SPY": 2, "AAPL": 1}
    price_dict = {"SPY": 100, "AAPL": 90}
    # Act
    equity = acct.get_equity(price_dict)
    # Assert
    assert equity == 1790  # 1000 + 500 + (2 * 100) + (1 * 90)

def test_margin_account_get_maintenance_requirement():
    # Arrange
    acct = MarginAccount()
    acct.holdings = {"SPY": 2, "AAPL": -1}  # Long SPY, Short AAPL
    price_dict = {"SPY": 100, "AAPL": 90}
    # Act
    req = acct.get_maintenance_requirement(price_dict)
    # Assert
    assert req == 77  # (2 * 100 * 0.25) + (1 * 90 * 0.3)

def test_margin_account_get_maintenance_excess():
    # Arrange
    acct = MarginAccount()
    acct.set_cash(1000)
    acct.margin_balance = 500
    acct.holdings = {"SPY": 2, "AAPL": -1}
    price_dict = {"SPY": 100, "AAPL": 90}
    # Act
    excess = acct.get_maintenance_excess(price_dict)
    # Assert
    assert excess == 1533  # 1610 equity (1000 cash + 500 margin + 200 SPY - 90 AAPL) - 77 maintenance requirement

def test_margin_account_get_open_order_maint_req():
    # Arrange
    acct = MarginAccount()
    price_dict = {"SPY": 100, "AAPL": 90}
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(MarketOrder("456", "AAPL", 1, "sell", "day", short=True))
    # Act
    req = acct.get_open_order_maint_req(price_dict)
    # Assert
    assert req == 77  # (2 * 100 * 0.25) + (1 * 90 * 0.3)

def test_margin_account_get_open_order_initial_req():
    # Arrange
    acct = MarginAccount()
    price_dict = {"SPY": 100, "AAPL": 90}
    acct.oms.new_open_order(MarketOrder("123", "SPY", 2, "buy", "day"))
    acct.oms.new_open_order(MarketOrder("456", "AAPL", 1, "sell", "day", short=True))
    # Act
    req = acct.get_open_order_initial_req(price_dict)
    # Assert
    assert req == 145  # (2 * 100 * 0.5) + (1 * 90 * 0.5)

if __name__ == "__main__":
    test_margin_account_get_open_order_initial_req()
    test_margin_account_get_open_order_maint_req()
    test_margin_account_get_maintenance_requirement()
    test_margin_account_get_maintenance_excess()
    test_margin_account_get_equity()
    test_margin_account_get_cash_available_to_invest()
    test_margin_account_initialization()
    test_cash_account_get_cash_available_to_invest()
    test_account_get_portfolio_value_missing_price()
    test_account_get_portfolio_value()
    test_account_withdraw_cash()
    test_account_deposit_cash()
