import os
import yfinance as yf
from datetime import datetime

with open('datasets/symbols.csv') as f:
    lines = f.read().splitlines()
    for symbol in lines:
        end_date = datetime.today().strftime('%Y-%m-%d')
        data = yf.download(symbol, start="2020-05-1", end=end_date)
        data.to_csv('datasets/squeeze/{}.csv'.format(symbol));