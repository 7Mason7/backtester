# class containing the blueprint for a fake brokerage account
from backtester.brokerage.order_management_system import OMS
from backtester.brokerage.order import *

class Account:
    """
    The Account class is the base representation of what a basic account would contain.
    This includes the cash, holdings, and a log of activity. 

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities.
    activity : list
        A list recording account activities (e.g., trades, deposits).
    oms : OMS
        The order management system object used to store and manage orders.
    """
    def __init__(self):
        self.cash: float = 0
        self.holdings: dict = {}
        self.activity: list = []
        self.oms = OMS()

    def set_cash(self, cash: float):
        """Set the cash balance to a specific amount."""
        self.cash = cash

    def deposit_cash(self, cash: float):
        """Add cash to the account."""
        self.cash += cash

    def withdraw_cash(self, cash: float):
        """Remove cash from the account."""
        self.cash -= cash

    def get_portfolio_value(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total portfolio value including cash and positions.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total portfolio value.
        """
        portfolio_value = self.cash
        for symbol, quantity in self.holdings.items():
            if symbol not in price_dict:
                raise KeyError(f"Missing price for symbol: {symbol}")
            portfolio_value += quantity * price_dict[symbol]
        return portfolio_value

    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total cash available for new investments.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The amount of cash available for new investments.
        """
        return self.cash - self.get_open_order_cost(price_dict)

    def get_open_order_cost(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total cost of all open orders in the account.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total cost of all open orders.
        """
        order_cost = 0.0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy':
                if isinstance(order, MarketOrder):
                    if order.symbol not in price_dict:
                        raise KeyError(f"Missing price for symbol: {order.symbol}")
                    order_cost += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    if order.limit_price is None:
                        raise ValueError(f"Limit order {order.order_id} has no limit price")
                    order_cost += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    if order.stop_price is None:
                        raise ValueError(f"Stop order {order.order_id} has no stop price")
                    order_cost += order.quantity * order.stop_price
                else:
                    if order.symbol not in price_dict:
                        raise KeyError(f"Missing price for symbol: {order.symbol}")
                    order_cost += order.quantity * price_dict[order.symbol]
        return order_cost


class CashAccount(Account):
    """
    A cash account implementation for trading strategies.

    This class extends the base Account class to provide cash-only trading capabilities,
    where positions can only be opened with available cash (no margin/leverage).
    It supports various order types including Market, Limit, and Stop orders.
    """
    pass  # Inherits all functionality from Account class


class MarginAccount(Account):
    """
    A margin account implementation for trading strategies.

    This class extends the base Account class to provide margin trading capabilities,
    allowing for both long and short positions with leverage. It supports various
    order types including Market, Limit, and Stop orders, and implements margin
    requirement calculations for both initial and maintenance requirements.

    Attributes
    ----------
    margin_balance : float
        The total margin balance, which can be positive (margin credit) or negative
        (margin debit).
    margin_requirements : dict
        Dictionary containing margin requirement percentages:
        - initial_long: Initial margin requirement for long positions (default: 0.5 or 50%)
        - initial_short: Initial margin requirement for short positions (default: 0.5 or 50%)
        - maint_long: Maintenance margin requirement for long positions (default: 0.25 or 25%)
        - maint_short: Maintenance margin requirement for short positions (default: 0.3 or 30%)
    """
    def __init__(self):
        super().__init__()
        self.margin_balance: float = 0.0
        self.margin_requirements: dict[str, float] = {
            'initial_long': 0.5,
            'initial_short': 0.5,
            'maint_long': 0.25,
            'maint_short': 0.3,
        }

    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total cash available for new investments including margin.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The amount of cash available for new investments including margin.
        """
        return self.cash + self.margin_balance - self.get_open_order_cost(price_dict)

    def get_open_order_maint_req(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the maintenance margin requirement for all open orders.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total maintenance margin requirement for open orders.
        """
        order_req = 0.0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy' and not order.short:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['maint_long'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['maint_long'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['maint_long'] * order.stop_price * order.quantity
            elif order.direction == 'sell' and order.short:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['maint_short'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['maint_short'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['maint_short'] * order.stop_price * order.quantity
        return order_req

    def get_open_order_initial_req(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the initial margin requirement for all open orders.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total initial margin requirement for open orders.
        """
        order_req = 0.0
        for order in self.oms.open_orders.values():
            if order.direction == 'buy' and not order.short:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['initial_long'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['initial_long'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['initial_long'] * order.stop_price * order.quantity
            elif order.direction == 'sell' and order.short:
                if isinstance(order, MarketOrder):
                    order_req += self.margin_requirements['initial_short'] * price_dict[order.symbol] * order.quantity
                elif isinstance(order, LimitOrder):
                    order_req += self.margin_requirements['initial_short'] * order.limit_price * order.quantity
                elif isinstance(order, StopOrder):
                    order_req += self.margin_requirements['initial_short'] * order.stop_price * order.quantity
        return order_req

    def get_equity(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total equity in the account.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total equity in the account.
        """
        equity = self.cash + self.margin_balance
        for symbol, quantity in self.holdings.items():
            equity += quantity * price_dict[symbol]
        return equity

    def get_maintenance_requirement(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total maintenance margin requirement for all positions.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The total maintenance margin requirement for all positions.
        """
        req = 0.0
        for symbol, quantity in self.holdings.items():
            if quantity > 0:
                req += self.margin_requirements['maint_long'] * quantity * price_dict[symbol]
            elif quantity < 0:
                req += self.margin_requirements['maint_short'] * abs(quantity) * price_dict[symbol]
        return req

    def get_maintenance_excess(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the excess equity above the maintenance requirement.

        Parameters
        ----------
        price_dict : dict[str, float]
            Dictionary mapping security symbols to their current prices.

        Returns
        -------
        float
            The excess equity above maintenance requirements. Negative values
            indicate a maintenance call.
        """
        return self.get_equity(price_dict) - self.get_maintenance_requirement(price_dict)



