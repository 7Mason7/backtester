from .order import *

class OMS:
    """
    OMS (Order Management System) is used to simulate the logic for orders.
    """

    def check_fill(self, price: float, order: Order)-> bool:
        """
        Pass a price to check an order if it's due for a fill.

        Parameters
        ----------
        price : float, required
            The price you want to check the order against.
        order : Order, required
            The order you want to check.
        """
        if order.status == "Open"

    