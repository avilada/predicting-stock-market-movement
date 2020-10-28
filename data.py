
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler


data_source = 'Kaggle'

if data_source == 'alphavantage':
    api_key = 'AEV4EE3TRUSE6CRG'
    ticker = "AAl"

    url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)
    file_to_save = 'market_data-%s.csv'%ticker 

    #getting data from url, storing values to a Pandas dataframe
    if not os.path.exists(file_to_save):
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())
            #extract stock market data
            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
            for k,v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                    float(v['4. close']),float(v['1. open'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        print('Data saved to : %s'%file_to_save)        
        df.to_csv(file_to_save)
    else: 
        print('File already exists')
        df = pd.read_csv(file_to_save)
else:
    df = pd.read_csv(os.path.join('Stocks','hpq.us.txt'),delimiter=',',usecols=['Date','Open','High','Low','Close'])
    print('Loaded data from the Kaggle repository')
    

high_prices = df.loc[:, 'High'].as_matrix()
low_prices = df.loc[:, 'Low'].as_matrix()
mid_prices = ((high_prices + low_prices) / 2.0)

train_data = mid_prices[:1100]
test_data = mid_prices[1100:]
