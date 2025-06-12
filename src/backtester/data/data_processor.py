"""
Work in progress. This module will be used to process data from CSV files and Pandas DataFrames.
"""

from pathlib import Path

import pandas as pd

class DataProcessor:

    def __init__(self) -> None:
        self.data_sources: dict[str, pd.DataFrame] = {}
        self.processed_data: Optional[pd.DataFrame] = None

    def add_csv_data(self, source_name: str, file_path: str) -> None:
        self.data_sources[source_name] = pd.read_csv(file_path)
        
        