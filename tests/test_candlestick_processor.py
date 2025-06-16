from backtester.simulation.data_processor import CandlestickProcessor
import pandas as pd

def test_add_data_frame():
    # Arrange
    df = pd.DataFrame(
        {
        'date': ['2023-01-01', '2023-01-02'],
        'opening_price': [100, 101],
        'highest': [102, 103],
        'lowest': [99, 100],
        'closing_price': [101, 102]
        }
    )
    processor = CandlestickProcessor()
    correct_columns = pd.Index(['open', 'high', 'low', 'close'])
    
    # Attempt
    processor.add_data_frame('XYZ', df, 'date', 'opening_price', 'highest', 'lowest', 'closing_price')
    
    # Assert
    result_df = processor.data_sources['XYZ']
    assert result_df.columns.equals(correct_columns), \
        f"Expected columns {correct_columns}, but got {result_df.columns}"
    assert result_df.shape == (2, 4), \
        f"Expected shape (2, 4), but got {result_df.shape}"
    assert result_df.index.equals(pd.DatetimeIndex(['2023-01-01', '2023-01-02'])), \
        f"Expected index {pd.DatetimeIndex(['2023-01-01', '2023-01-02'])}, but got {result_df.index}"
    assert result_df.iloc[0]['open'] == 100, \
        f"Expected open value 100, but got {result_df.iloc[0]['open']}"
    assert result_df.iloc[0]['high'] == 102, \
        f"Expected high value 102, but got {result_df.iloc[0]['high']}"
    assert result_df.iloc[0]['low'] == 99, \
        f"Expected low value 99, but got {result_df.iloc[0]['low']}"
    assert result_df.iloc[0]['close'] == 101, \
        f"Expected close value 101, but got {result_df.iloc[0]['close']}"

if __name__ == "__main__":
    test_add_data_frame()

