
from enum import Enum

class OMS:
    """
    OMS (Order Management System) is used to simulate the logic for orders.
    """
    def order_create(self):
        """
        Adds an existing Order object to the Account's open_orders list.

        Parameters
        ----------
        order : Order, required
            An instance of the Order class to be added to open_orders.
        """

    def order_cancel(self, order_index: int):
        """
        Cancels a given order at the selected index within the open_orders attribute.

        Parameters
        ----------
        order_index : int, required
            The index of hte order within the Account.open_orders list.
        """

    def check_fill(self, current_price: float):
        """
        Pass a price to check all open_orders for execution. If the order is executed, the order is removed and added to activity.

        Parameters
        ----------
        current_price : float, required
            The price you want to check the order against.
        """

    