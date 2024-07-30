# Databricks notebook source
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
import warnings
import seaborn as sns; sns.set()

%matplotlib inline
warnings.filterwarnings('ignore')

# COMMAND ----------

import yfinance as yf
#yf.pdr_override()

# COMMAND ----------

stocks = ['AAPL','IBM','MSFT','INTC','^GSPC']
start = datetime.datetime(2021,1,1)
end = datetime.datetime(2021,4,1)
stock_prices = yf.download(stocks,start=start,end = end, interval='1d')

# COMMAND ----------

stock_prices.head()

# COMMAND ----------

stock_prices = stock_prices['Close']

# COMMAND ----------

stock_prices.dropna(inplace=True)

# COMMAND ----------

stock_prices.head()

# COMMAND ----------

#Summary statistics
##Shows the price of the S&P 500 is way different from the rest of these stocks. (Apple, IBM, Intel, Microsoft)
stock_prices.describe()

# COMMAND ----------

#Rename target column ^GSPC 
stock_prices = stock_prices.rename({'^GSPC' : 'GSPC'}, axis = 'columns')

# COMMAND ----------

# MAGIC %pip install fredapi

# COMMAND ----------

#Connect to the Federal Reserve Economic Database (FRED)
from fredapi import Fred
fred = Fred(api_key='b6804aa5cab119daedf45b9e29bb1391')

# COMMAND ----------

fred.search('risk free')

# COMMAND ----------

risk_free = fred.get_series('DGS3MO')
risk_free = risk_free['2021-01-01' : '2021-04-01']
