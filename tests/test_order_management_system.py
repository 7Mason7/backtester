from backtester.brokerage.order_management_system import OMS
from backtester.brokerage.order import *

def test_order_management_system_new_open_order():
    # Arrange:
    oms = OMS()
    order = MarketOrder("123", "SPY", 10, "sell", time_in_force="day")
    # Act:
    oms.new_open_order(order)
    # Assert:
    assert oms.open_orders["123"] is order

def test_order_management_system_cancel_order():
    # Arrange:
    oms = OMS()
    orderID = "404"
    order = Order(orderID, "AAPL", 1, "sell", "day")
    # Act:
    oms.new_open_order(order)
    oms.cancel_order(orderID)
    # Assert:
    assert oms.cancelled_orders[orderID] is order
    assert len(oms.open_orders) == 0

if __name__ == "__main__":
    test_order_management_system_new_open_order()
    test_order_management_system_cancel_order()
    