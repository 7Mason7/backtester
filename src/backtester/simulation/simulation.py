import pandas as pd

class Simulation:
    def __init__(self):
        self.candle_data: pd.DataFrame
    
    
    # Attributes: 
    #   Pandas Dataframe of each security, normalized so the indicies match by timestamp.
    #   Price dictionary. For each security time series, create a price dictionary and update per tick.
    #   Your account
    #   Steps = The number of intervals within the price df
    # Methods:
    #   Step forward
    #   Return price data
    #   Place an order

