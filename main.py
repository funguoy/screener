"""
Created by: Jordan Loves
October 2021
"""
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import yfinance as yf
import yahoo_fin.stock_info as si
import datetime as dt
import time
from get_all_tickers import get_tickers as gt
yf.pdr_override()

ticker_list = si.tickers_nasdaq()
#get rid of warrants, otc or unwanted names
ticker_list = [x[:4] if len(x)>4 else x for x in ticker_list]
#print(len(tickers))

# A loop will take way too long, will remove all stocks with market cap > 1000M
# This code actually takes far too long. I think there's a cap on num requests
tickers = []
"""for ticker in ticker_list[:10]:  # Going to shorten because program is taking too long to run
    try:
        if (yf.Ticker(ticker).info['marketCap'] < 1000000000):
            tickers.append(ticker)
    except:
        continue

print(tickers)
print(len(tickers))"""

# Set dates
start = dt.datetime(2021, 10, 1)
end = dt.datetime.now()

# Loop scrapes info for each stock
app_data = []
for ticker in ticker_list[:500]: # Code takes a while to run, will use a subset of the list for now cus slow
    try:
        df_tick = pdr.DataReader(ticker, 'yahoo', start, end)
        df_tick['symbol'] = ticker
        df_tick['gap_multiple'] = df_tick.Open.div(df_tick.Close.shift(1))
        df_tick['percent_change'] = df_tick.gap_multiple.apply(lambda x: (x * 100) - 100)
        #df_tick['date'] = df_tick.index
        df_tick = df_tick.reset_index()
        df_tick = df_tick[df_tick.percent_change > 10]  # Only want rows where percent_change is > 10
        app_data.append(df_tick)
    except:
        print('the symbol ' + ticker + ' is not found')
        continue

app_data = pd.concat(app_data)
app_data = app_data.reset_index()  # Index repeats for each ticker, changed that here
print(app_data.info())
print(app_data.head())

#app_data = app_data[app_data.percent_change > 10]

app_data.to_csv('stock_data.csv')



