from backtester.Account import Account
from backtester.Order import Order

def test_create_order():
    # Given
    acct = Account(1000)
    expected_cash = 890
    expected_activity = [-110]
    expected_holdings = {'SPY': 10}
    # When
    acct.order_create(Order(symbol="SPY", quantity=10, order_type="Limit", price=11))
    current_price = 10
    acct.order_check(current_price)
    # Then
    assert acct.cash == expected_cash
    assert acct.activity == expected_activity
    assert acct.holdings == expected_holdings