from ..src.backtester.account.account import Account

def account_test_deposit_cash():
    # Arrange:
    acct = Account()

    # Act:
    acct.deposit_cash(100)

    # Assert:
    assert acct.cash == 100, "Deposit did not update balance correctly."

def account_test_withdraw_cash():
    # Arrange:
    acct = Account()

    # Act:
    acct.withdraw_cash(100)

    # Assert:
    assert acct.cash == -100, "Withdraw did not update balance correctly."


def account_test_get_portfolio_value():
    # Arrange:
    acct = Account()
    acct.set_cash = 100

    # Act:
    portfolioVal = acct.get_portfolio_value

    # Assert:
    assert portfolioVal == 100, "get_portfolio_value did not return the correct value."