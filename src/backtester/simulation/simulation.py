import pandas as pd

class Simulation:
    def __init__(
        self,
        historical_data: HistoricalData,
        account: Account,  # Can be either BacktestCashAccount or BacktestMarginAccount
        start_date: pd.Timestamp = None,
        end_date: pd.Timestamp = None
    ):
        self.historical_data = historical_data
        self.account = account
        self.start_date = start_date or historical_data.time_index[0]
        self.end_date = end_date or historical_data.time_index[-1]
        self.current_time_index = 0
        self.price_dict = {}
        self.performance_history = []
        
    def run(self):
        """Execute the full simulation"""
        while self.current_time_index < len(self.historical_data.time_index):
            self.step()
            self.current_time_index += 1
            
    def step(self):
        """Process one time interval"""
        # Update price dictionary
        self._update_prices()
        
        # Process open orders
        self._process_orders()
        
        # Update account metrics
        self._update_account()
        
        # Record performance
        self._record_performance()
        
    def place_order(self, order: Order):
        """Place a new order"""
        self.account.oms.place_order(order)
        
    def _update_prices(self):
        """Update current prices for all securities"""
        current_time = self.historical_data.time_index[self.current_time_index]
        self.price_dict = {symbol: data.loc[current_time] for symbol, data in self.historical_data.data.items()}
        
    def _process_orders(self):
        """Process and execute open orders"""
        current_time = self.historical_data.time_index[self.current_time_index]
        
        # Get all open orders
        open_orders = list(self.account.oms.open_orders.values())
        
        for order in open_orders:
            # Check if order can be executed
            if self._can_execute_order(order):
                self._execute_order(order)
                
    def _can_execute_order(self, order: Order) -> bool:
        """Check if order can be executed based on current prices"""
        current_price = self.price_dict[order.symbol]
        
        if isinstance(order, MarketOrder):
            return True
            
        elif isinstance(order, LimitOrder):
            if order.direction == 'buy':
                return current_price <= order.limit_price
            else:  # sell
                return current_price >= order.limit_price
                
        elif isinstance(order, StopOrder):
            if order.direction == 'buy':
                return current_price >= order.stop_price
            else:  # sell
                return current_price <= order.stop_price
                
        return False
        
    def _execute_order(self, order: Order):
        """Execute an order and update account"""
        current_price = self.price_dict[order.symbol]
        
        # Update order status
        order.status = "executed"
        order.executed_price = current_price
        
        # Move order from open to executed
        self.account.oms.executed_orders[order.order_id] = order
        del self.account.oms.open_orders[order.order_id]
        
        # Update account holdings
        if order.direction == 'buy':
            self.account.holdings[order.symbol] = self.account.holdings.get(order.symbol, 0) + order.quantity
            self.account.cash -= current_price * order.quantity
        else:  # sell
            self.account.holdings[order.symbol] = self.account.holdings.get(order.symbol, 0) - order.quantity
            self.account.cash += current_price * order.quantity
            
        # If it's a margin account, update margin balance
        if isinstance(self.account, BacktestMarginAccount):
            # Add margin balance update logic here
            pass
        
    def _update_account(self):
        """Update account metrics"""
        pass
        
    def _record_performance(self):
        """Record current performance metrics"""
        pass
        
    def get_performance_metrics(self):
        """Calculate and return performance metrics"""
        pass

