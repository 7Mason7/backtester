from backtester.Account.Account import Account
from backtester.Orders.Order import Order

def test():
    acct = Account()

    acct.order_create(Order(symbol="SPY", quantity=10, order_type="Limit", price=11))

    current_price = 10

    acct.order_check(current_price)

    print(acct.cash)
    print(acct.activity)
    print(acct.holdings)

test()