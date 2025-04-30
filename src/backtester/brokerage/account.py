# class containing the blueprint for a fake brokerage account

class Account:
    """
    The Account class is the a representation of what a basic account would contain.
    This includes the cash, holdings, and a log of activity. 
    Not intended for a backtest and should be used as a base class.

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities.
    activity : list
        A list recording account activities (e.g., trades, deposits).
    """
    def __init__(self):
        self.cash: float = 0
        self.holdings: dict = {}
        self.activity: list = []

    def set_cash(self, cash: float):
        self.cash = cash

    def deposit_cash(self, cash: float):
        self.cash += cash

    def withdraw_cash(self, cash: float):
        self.cash -= cash

    def get_portfolio_value(self, priceDict: dict) -> float:
        portfolio_value = self.cash
        for symbol, quantity in self.holdings:
            if symbol not in priceDict:
                raise KeyError(f"Missing price for symbol: {symbol}")
            portfolio_value += quantity * priceDict[symbol]
        return portfolio_value



