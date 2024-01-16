import os
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

def plot(df):
    candlestick = go.Candlestick(x=df['Date'],
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'])
    upper_band = go.Scatter(x=df['Date'], y=df['upperband'], name='Uper Bollinger Band')
    lower_band = go.Scatter(x=df['Date'], y=df['lowerband'], name='Lower Bollinger Band')
    lower_keltner_channel = go.Scatter(x=df['Date'], y=df['lower_keltner'], name='Lower Keltner Channel')
    upper_keltner_channel = go.Scatter(x=df['Date'], y=df['upper_keltner'], name='Upper Keltner Channel')
    fig = go.Figure(data=[candlestick, upper_band, lower_band, lower_keltner_channel, upper_keltner_channel])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    
    # fig.show()
    return fig

def get_squeeze(ticker):
    for filename in os.listdir('datasets/squeeze'):
        symbol = filename.split('.')[0]
        if symbol == ticker:
            df = pd.read_csv('datasets/squeeze/{}'.format(filename))
            if df.empty:
                continue
            
            # Calculate 20 day simple moving average
            df['20sma'] = df['Close'].rolling(window=20).mean()
            
            # Calculating standard deviation
            df['std'] = df['Close'].rolling(window=20).std()
            df['lowerband'] = df['20sma'] - (2 * df['std'])
            df['upperband'] = df['20sma'] + (2 * df['std'])
            
            # True range
            df['TR'] = abs(df['High']-df['Low'])
            
            # Average True Range
            df['ATR'] = df['TR'].rolling(window=20).mean()
            
            df['lower_keltner'] = df['20sma'] - df['ATR'] * 1.5
            df['upper_keltner'] = df['20sma'] + df['ATR'] * 1.5
            
            def in_squeeze(df):
                return df['lowerband'] > df['lower_keltner'] and df['upperband'] < df['upper_keltner']
            
            df['squeeze_on'] = df.apply(in_squeeze, axis=1)
            return df


get_squeeze("DRI")