import csv

def read_csv(path: str):
    with open(path, 'r') as csv_file:
        return csv.reader(csv_file)