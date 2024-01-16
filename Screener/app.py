from flask import Flask, redirect, render_template, request, url_for
from patterns import patterns
import pandas as pd
from plotly.io import to_html
from squeeze import *
import matplotlib
matplotlib.use('agg')
from talib import _ta_lib as talib
import os, csv
import yfinance as yf
# from flask_script import Manager
from datetime import datetime
import quantstats as qs
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    pattern = request.args.get('pattern', False)
    stocks = {}
    stocks_squeeze = {}
    in_squeeze = False
    
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
            stocks_squeeze[row[0]] = False
    flag = False
    if pattern:
        datasets = os.listdir('datasets/daily')
        for dataset in datasets:
            df = pd.read_csv('datasets/daily/{}'.format(dataset))
            if pattern != "See All":
                pattern_function = getattr(talib, pattern)
                
                symbol = dataset.split('.')[0]
                
                
                try:
                    # print(pattern_function)
                    result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                    last = result.tail(1).values[0]
                    # print(last)
                    if last > 0:
                        stocks[symbol][pattern] = 'Bearish'
                        flag = True
                    elif last<0:
                        stocks[symbol][pattern] = 'Bullish'
                        flag = True
                    else:
                        stocks[symbol][pattern] = None
                        
                    new_df = get_squeeze(ticker=symbol)
                    in_squeeze = new_df.iloc[-1][-1]
                    stocks_squeeze[symbol] = in_squeeze
                except:
                    pass
                
    # print(stocks)  
    # print(stocks_squeeze)   
    if pattern=="See All" or not pattern:
        flag = True
    # print(stocks)  
    return render_template('index.html', patterns=patterns, stocks=stocks, curr_pattern=pattern, stocks_squeeze = stocks_squeeze, flag=flag)

@app.route('/snapshot')
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            end_date = datetime.today().strftime('%Y-%m-%d')
            data = yf.download(symbol, start="2020-01-01", end=end_date)
            data.to_csv('datasets/daily/{}.csv'.format(symbol))
            
    return {
        "code": "success"
    }
        
        
# Modify your tearsheet() route to handle the new form input
@app.route('/tearsheet', methods=['GET', 'POST'])
def tearsheet():
    try:
        qs.extend_pandas()
        stock_to_analyze = request.args.get('stock', None)
        pattern = request.args.get('pattern', None)

        if request.method == 'POST':
            compare_stock = request.form.get('compare_stock')
            return redirect(url_for('tearsheet', stock=stock_to_analyze, pattern=pattern, compare_stock=compare_stock))

        compare_stock = request.args.get('compare_stock', None)

        if stock_to_analyze:
            with app.app_context():
                stock = qs.utils.download_returns(stock_to_analyze)
                stock_to_compare = "SPY"

                if compare_stock:
                    stock_to_compare = compare_stock

                qs.reports.html(returns=stock, benchmark=stock_to_compare, title="{} vs {}".format(stock_to_analyze, stock_to_compare), output="static/tearsheet_{}.html".format(stock_to_analyze))
                tearsheet_file_path = "static/tearsheet_{}.html".format(stock_to_analyze)

                with open(tearsheet_file_path, 'r') as tearsheet_file:
                    tearsheet_content = tearsheet_file.read()

                return render_template('tearsheet.html', stock=stock_to_analyze, tearsheet_content=tearsheet_content, pattern=pattern)
    except Exception as e:
        return render_template('error.html', message=f"Failed to generate tear sheet for {stock_to_analyze}: {str(e)}")



@app.route('/ttmsqueeze')
def ttmsqueeze():
    ticker = request.args.get('stock', None)
    if ticker:
        try:
            new_df = get_squeeze(ticker=ticker)
            fig = plot(new_df)
            fig_html = to_html(fig, full_html=False)
            return render_template('squeeze.html', fig_html=fig_html, stock=ticker)
        except Exception as e:
            return render_template('error.html', message=f"Failed to generate squeeze for {ticker}: {str(e)}")

# manager = Manager(app)
