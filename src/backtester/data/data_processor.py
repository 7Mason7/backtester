"""
Work in progress. This module will be used to process data from CSV files and Pandas DataFrames.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

class CandlestickProcessor:
    """
    This class is used to process candlestick data from CSV files and Pandas DataFrames for backtesting.
    """

    def __init__(self) -> None:
        self.data_sources: dict[str, pd.DataFrame] = {}
        self.processed_data: Optional[pd.DataFrame] = None

    def add_csv_data(self, 
                     source_name: str, 
                     file_path: Path | str,
                     timestamp_column: str,
                     open_column: str,
                     high_column: str,
                     low_column: str,
                     close_column: str,
                     ) -> None:
        """
        Add data from a CSV file.
        Args:
            source_name: Name of the data source.
            file_path: Path to the CSV file.
            timestamp_column: Name of the timestamp column.
            open_column: Name of the open column.
            high_column: Name of the high column.
            low_column: Name of the low column.
            close_column: Name of the close column.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        self.data_sources[source_name] = pd.read_csv(file_path)

    def add_data_frame(self, source_name: str, df: pd.DataFrame) -> None:
        self.data_sources[source_name] = df
        
    def _merge_by_timestamp(self) -> pd.DataFrame:
        for data_source in self.data_sources:


        