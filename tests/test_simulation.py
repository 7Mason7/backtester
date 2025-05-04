from ..src.backtester.brokerage.backtest_account import BacktestCashAccount
from ..src.backtester.simulation.csv_helper import read_csv

def test_simulation():
    # feed in the data
    acct = BacktestCashAccount()
    acct.set_cash(1000)
    csv = read_csv("...backtester/SPY.csv")
    print("CSV content", csv)

    for line in csv:
        print(line)


test_simulation()