# common orders

class Order:
    """
    A class for common order types.
    """
    def __init__(self, symbol: str, quantity: float, order_type: str = "Market", time_in_force: str = "GTC", price: float = None):
        """
        Parameters
        ----------
        order_type : str, optional
            The type of order. Valid options are "Market", "Limit", or "Stop".
            Defaults to "Market"
        time_in_force : str, optional
            Duration of the order. Valid options are "GTC" or "Day".
            Defaults to "GTC"
        price : float, optional
            The limit or stop price. Must be used when order_type = Limit or Stop.
            Defaults to None

        Raises
        ------
        ValueError
            If order_type is "Limit" or "Stop", and price is None.
        """
        if (order_type == "Limit" or order_type == "Stop") and price == None:
            raise ValueError("order_type = Limit or Stop but no price specified!")
        
        self.symbol: str = symbol
        self.quantity: float = quantity
        self.order_type: str = order_type
        self.time_in_force: str = time_in_force
        self.price: float = price


    def status(self):
        match self.order_type:
            case "Market":
                return
            case "Limit":
                return
            case "Stop":
                return
            





x = Order(order_type="Limit", price=10)

print(x.order_type)
