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
    correct_columns = pd.Index([
        'timestamp',
        'open',
        'high',
        'low',
        'close'
        ])
    # Attempt
    processor.add_data_frame('XYZ', df, 'date', 'opening_price', 'highest', 'lowest', 'closing_price')
    # Assert
    print(processor.data_sources['XYZ'].columns)

