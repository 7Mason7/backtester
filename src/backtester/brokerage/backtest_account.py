from .account import Account
from .order_management_system import OMS
from .order import *

class BacktestCashAccount(Account):
    """
    A cash account implementation for backtesting trading strategies.

    This class extends the base Account class to provide cash-only trading capabilities,
    where positions can only be opened with available cash (no margin/leverage).
    It supports various order types including Market, Limit, and Stop orders.

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities. All positions
        must be fully funded by available cash.
    activity : list
        A list recording account activities (e.g., trades, deposits).
    oms : OMS
        The order management system object used to store and manage orders.

    Methods
    -------
    get_cash_available_to_invest(price_dict)
        Calculates available cash excluding the cost of open orders.
    get_open_order_cost(price_dict)
        Calculates the total cost of all open orders.
    """

    def __init__(self):
        super().__init__()
        self.oms = OMS()

    def get_cash_available_to_invest(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total cash available for new investments.

        This method considers the current cash balance and subtracts the cost
        of any open orders to determine the actual available cash for new positions.

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

        This method sums up the cost of all open buy orders based on their
        type (Market, Limit, or Stop) and current market prices.

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
                    order_cost += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    order_cost += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    order_cost += order.quantity * order.stop_price
                else:
                    order_cost += order.quantity * price_dict[order.symbol]
        return order_cost

class BacktestMarginAccount(Account):
    """
    A margin account implementation for backtesting trading strategies.

    This class extends the base Account class to provide margin trading capabilities,
    allowing for both long and short positions with leverage. It supports various
    order types including Market, Limit, and Stop orders, and implements margin
    requirement calculations for both initial and maintenance requirements.

    Attributes
    ----------
    cash : float
        The current cash balance in the account.
    holdings : dict
        A dictionary mapping security symbols to their quantities. Positive values
        indicate long positions, negative values indicate short positions.
    activity : list
        A list recording account activities (e.g., trades, deposits, margin calls).
    oms : OMS
        The order management system object used to store and manage orders.
    margin_balance : float
        The total margin balance, which can be positive (margin credit) or negative
        (margin debit).
    margin_requirements : dict
        Dictionary containing margin requirement percentages:
        - initial_long: Initial margin requirement for long positions (default: 0.5 or 50%)
        - initial_short: Initial margin requirement for short positions (default: 0.5 or 50%)
        - maint_long: Maintenance margin requirement for long positions (default: 0.25 or 25%)
        - maint_short: Maintenance margin requirement for short positions (default: 0.3 or 30%)

    Methods
    -------
    get_cash_available_to_invest(price_dict)
        Calculates available cash including margin balance and excluding open orders.
    get_open_order_cost(price_dict)
        Calculates the total cost of all open orders.
    get_open_order_maint_req(price_dict)
        Calculates maintenance margin requirements for open orders.
    get_open_order_initial_req(price_dict)
        Calculates initial margin requirements for open orders.
    get_equity(price_dict)
        Calculates total account equity including cash, margin balance, and positions.
    get_maintenance_requirement(price_dict)
        Calculates total maintenance margin requirement for all positions.
    get_maintenance_excess(price_dict)
        Calculates the excess equity above maintenance requirements.
    """
    def __init__(self):
        super().__init__()
        self.oms = OMS()
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

        This method considers the current cash balance, margin balance, and subtracts
        the cost of any open orders to determine the actual available cash for new positions.

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

    def get_open_order_cost(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the total cost of all open orders in the account.

        This method sums up the cost of all open buy orders based on their
        type (Market, Limit, or Stop) and current market prices.

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
                    order_cost += order.quantity * price_dict[order.symbol]
                elif isinstance(order, LimitOrder):
                    order_cost += order.quantity * order.limit_price
                elif isinstance(order, StopOrder):
                    order_cost += order.quantity * order.stop_price
                else:
                    order_cost += order.quantity * price_dict[order.symbol]
        return order_cost

    def get_open_order_maint_req(self, price_dict: dict[str, float]) -> float:
        """
        Calculate the maintenance margin requirement for all open orders.

        This method calculates the total maintenance margin requirement based on
        the type of order (long/short) and the applicable margin requirement percentage.

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

        This method calculates the total initial margin requirement based on
        the type of order (long/short) and the applicable margin requirement percentage.

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

        This method sums up the cash balance, margin balance, and the current
        market value of all positions.

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

        This method calculates the maintenance margin requirement for each position
        based on whether it's a long or short position and applies the appropriate
        margin requirement percentage.

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

        This method determines how much equity is available above the maintenance
        requirement. A negative value indicates a maintenance call.

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
    