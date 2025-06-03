from backtester.brokerage.backtest_account import BacktestCashAccount
import csv

def test_simulation():
    # feed in the data
    acct = BacktestCashAccount()
    acct.set_cash(1000)

    with open("SPY.csv", newline='') as csv_file:
        read = csv.reader(csv_file)

    



test_simulation()