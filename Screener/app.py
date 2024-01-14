from flask import Flask, render_template, request
from patterns import patterns
import pandas as pd
import matplotlib
matplotlib.use('agg')
from talib import _ta_lib as talib
import os, csv
import yfinance as yf
# from flask_script import Manager
import quantstats as qs
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    pattern = request.args.get('pattern', False)
    stocks = {}
    
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    if pattern:
        datasets = os.listdir('datasets/daily')
        for dataset in datasets:
            df = pd.read_csv('datasets/daily/{}'.format(dataset))
            pattern_function = getattr(talib, pattern)
            
            symbol = dataset.split('.')[0]
            
            try:
                # print(pattern_function)
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]
                # print(last)
                if last > 0:
                    stocks[symbol][pattern] = 'Bearish'
                elif last<0:
                    stocks[symbol][pattern] = 'Bullish'
                else:
                    stocks[symbol][pattern] = None
            except:
                pass
            
    return render_template('index.html', patterns=patterns, stocks=stocks, curr_pattern=pattern)

@app.route('/snapshot')
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            data = yf.download(symbol, start="2020-01-01", end="2023-08-08")
            data.to_csv('datasets/daily/{}.csv'.format(symbol))
            
    return {
        "code": "success"
    }
        
        
@app.route('/tearsheet')
def tearsheet():
    qs.extend_pandas()
    stock_to_analyze = request.args.get('stock', None)
    if stock_to_analyze:
        with app.app_context():
            stock = qs.utils.download_returns(stock_to_analyze)
            qs.reports.html(returns=stock,title="Tear sheet for {}".format(stock), output="static/tearsheet_{}.html".format(stock_to_analyze))
            tearsheet_file_path = "tearsheet_{}.html".format(stock_to_analyze)
            # print()
            with open(tearsheet_file_path, 'r') as tearsheet_file:
                tearsheet_content = tearsheet_file.read()
            return render_template('tearsheet.html', stock=stock_to_analyze, tearsheet_content=tearsheet_content)
    
    return render_template('error.html', message="Invalid request")

# manager = Manager(app)

# if __name__ == '__main__':
#     manager.run()