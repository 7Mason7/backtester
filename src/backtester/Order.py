# common orders

class Order:
    """
    A class for common order types.
    """
    def __init__(self, 
                 symbol: str, 
                 quantity: float, 
                 buy_or_sell: str = "Buy", 
                 order_type: str = "Market", 
                 time_in_force: str = "GTC", 
                 price: float = None
                 ):
        """
        Parameters
        ----------
        symbol : str, required
            The security's identifier.
        quantity : float, required
            The number of shares to purchase or sell.
        buy_or_sell : str, optional
            Valid options are "Buy" or "Sell".
            Defaults to "Buy".
        order_type : str, optional
            The type of order. Valid options are "Market", "Limit", or "Stop".
            Defaults to "Market"
        time_in_force : str, optional
            Duration of the order. Valid options are "GTC" or "Day".
            Defaults to "GTC".
        price : float, optional
            The limit or stop price. Must be used when order_type = Limit or Stop.
            Defaults to None.

        Attributes
        ----------
        status : str
            The status of the order. Can be "Open" or "Executed".
        executed_price : float
            The executed price. Starting value is None unless the check_fill method is invoked and the criteria is met.

        Raises
        ------
        ValueError
            If order_type is "Limit" or "Stop", and price is None.
        ValueError
            If order_type is "Market", and price is not None.
        """
        if (order_type == "Limit" or order_type == "Stop") and price == None:
            raise ValueError("order_type = Limit or Stop but no price specified!")
        if order_type == "Market" and price is not None:
            raise ValueError("order_type = Market but price specified!")
        
        self.buy_or_sell: str = buy_or_sell
        self.symbol: str = symbol
        self.quantity: float = quantity
        self.order_type: str = order_type
        self.time_in_force: str = time_in_force
        self.price: float = price
        self.status: str = "Open"
        self.executed_price: float = None


    def check_fill(self, current_price: float) -> str:
        """
        Checks if the order was filled based on inputted price.

        Parameters
        ----------
        current_price : float, required
            The current price used to check if the order will fill.
        """
        match self.order_type:
            case "Market":
                self.executed_price = current_price
                self.status = "Executed"
            case "Limit":
                if self.buy_or_sell == "Buy" and current_price <= self.price:
                    self.executed_price = self.price
                    self.status = "Executed"
                elif self.buy_or_sell == "Sell" and current_price >= self.price:
                    self.executed_price = self.price
                    self.status = "Executed"
            case "Stop":
                if self.buy_or_sell == "Buy" and current_price >= self.price:
                    self.executed_price = self.price
                    self.status = "Executed"
                elif self.buy_or_sell == "Sell" and current_price <= self.price:
                    self.executed_price = self.price
                    self.status = "Executed"
            
