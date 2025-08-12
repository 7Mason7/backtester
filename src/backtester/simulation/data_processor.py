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
        df = pd.read_csv(file_path)
        self.add_data_frame(source_name, df, timestamp_column, open_column, high_column, low_column, close_column)

    def add_data_frame(self,
                       source_name: str,
                       df: pd.DataFrame,
                       timestamp_column: str,
                       open_column: str,
                       high_column: str,
                       low_column: str,
                       close_column: str,
                       ) -> None:
        """
        Add data from a Pandas DataFrame.
        Args:
            source_name: Name of the data source.
            df: Pandas DataFrame.
            timestamp_column: Name of the timestamp column.
            open_column: Name of the open column.
            high_column: Name of the high column.
            low_column: Name of the low column.
            close_column: Name of the close column.
        """
        required_columns = [timestamp_column, open_column, high_column, low_column, close_column]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"df is missing {missing_columns}")
        
        col_mapper = {
            required_columns[0]: 'timestamp',
            required_columns[1]: 'open',
            required_columns[2]: 'high',
            required_columns[3]: 'low',
            required_columns[4]: 'close'
        }

        new_df = df[required_columns].rename(columns=col_mapper)B
        new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
        new_df.set_index('timestamp', inplace=True)
        self.data_sources[source_name] = new_df

    def merge_data(self) -> None:
        # merge the datasources into a singular df
        # loop through each df in data sources
        # find the beginning and end timestamp
        # if the next df has a beginning > the previous, set the beggining var = that beginning
        # if the next df has an end < the previous, set the end var = that end
        all_begin = None
        all_end = None

        for df in self.data_sources.values():
            this_begin = df.index.min()
            this_end = df.index.max()

            if all_begin is None:
                all_begin = this_begin
                all_end = this_end
            else:
                if this_begin > all_begin:
                    all_begin = this_begin
                if this_end < all_end:
                    all_end = this_end

        if all_begin >= all_end:
            self.processed_data = None
            return
        
        merged = None
        for df in self.data_sources.values():
            sliced_df = df.loc[all_begin:all_end]
            if merged is None:
                merged = sliced_df
            else:
                # functionality to merge
                pass
            

    """ def _resample_by_timestamp(self) -> pd.DataFrame:
        pass """ # will add functionality to resample to the highest timeframe