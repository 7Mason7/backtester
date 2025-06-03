from src.backtester.brokerage.account import Account

def test_account_deposit_cash():
    # Arrange:
    acct = Account()
    # Act:
    acct.deposit_cash(100)
    # Assert:
    assert acct.cash == 100

def test_account_withdraw_cash():
    # Arrange:
    acct = Account()
    # Act:
    acct.withdraw_cash(100)
    # Assert:
    assert acct.cash == -100


def test_account_get_portfolio_value():
    # Arrange:
    acct = Account()
    acct.set_cash(100)
    price_dict = {}
    # Act:
    portfolioVal = acct.get_portfolio_value(price_dict)
    # Assert:
    assert portfolioVal == 100