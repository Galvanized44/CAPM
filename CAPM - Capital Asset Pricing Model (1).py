# Databricks notebook source
# MAGIC %pip install yfinance fredapi

# COMMAND ----------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
import seaborn as sns;
import yfinance as yf

# COMMAND ----------

stocks = ['AAPL','IBM','MSFT','INTC','^GSPC']
start = datetime.datetime(2021,1,1)
end = datetime.datetime(2021,4,1)
stock_prices = yf.download(stocks,start=start,end = end, interval='1d')

# COMMAND ----------

stock_prices.head()

# COMMAND ----------

stock_prices = stock_prices['Close']
stock_prices.dropna(inplace=True)
stock_prices.head()

# COMMAND ----------

#Summary statistics
##Shows the price of the S&P 500 is way different from the rest of these stocks. (Apple, IBM, Intel, Microsoft)
stock_prices.describe()

# COMMAND ----------

#Rename target column ^GSPC 
stock_prices = stock_prices.rename({'^GSPC' : 'GSPC'}, axis = 'columns')

# COMMAND ----------

#Visualize the 4 stock prices and 1 market index
##Looks like all show positive trend except for Apple.. wah wah wah
for i in range(0, len(stock_prices.columns)):
    sns.set()
    plt.figure(figsize=(10, 10))
    #5 columns, 1 row, positioned top down 1-5
    plt.subplot(5, 1, i+1)
    plt.plot(stock_prices[stock_prices.columns[i]])
    plt.title("{}".format(stock_prices.columns[i]))
    plt.tight_layout()
    plt.show()

# COMMAND ----------

#Calculate correlation coefficients to see which variables if any are linearly related.
##Intel and the S&P500 seem to have a strong positive linear relationship. 
heat_corr = stock_prices.corr()
sns.heatmap(heat_corr, annot=True)
plt.title("Correlation Matrix")
plt.show()

# COMMAND ----------

##Calculate Excess Returns: Stock Returns - Risk Free Rate
#Pt1 - Risk Free Rate
#Connect to the Federal Reserve Economic Database (FRED)
from fredapi import Fred
fred = Fred(api_key='b6804aa5cab119daedf45b9e29bb1391')

# COMMAND ----------

#Look for a risk free asset (i.e., government backed)
fred.search('risk free')

# COMMAND ----------

#Get timeseries data for Jan21-April21
#DGS3MO - 3-Month Treasury Constant Maturity Rate
risk_free = fred.get_series('DGS3MO')
risk_free = risk_free['2021-01-01':'2021-04-01']
risk_free.head()

# COMMAND ----------

risk_free_2 = risk_free.dropna()

# COMMAND ----------

rf = risk_free / 90
rf = rf.dropna()

# COMMAND ----------

#Visualize the risk free asset rate data.
#This shows the interest rate/yield a person can expect from purchase to maturity (3months later) is trending down.
plt.plot(risk_free_2)
plt.xlabel('Date')
plt.ylabel('%')
plt.title('3-Month Treasury Constant Maturity Rate')
plt.xticks(rotation=90)
plt.show()

# COMMAND ----------

#Pt2 Stock Returns
returns = stock_prices.pct_change()
returns.dropna(inplace=True)
returns.head()

# COMMAND ----------

for i in stock_prices.columns:
  returns["excess_return_" + str(i)] = returns[i] - risk_free_2

# COMMAND ----------

print(returns)

# COMMAND ----------

#Pt2 Stock Returns
returned = stock_prices.pct_change()
returned.dropna(inplace=True)
returned.head()

# COMMAND ----------

for i in stock_prices.columns:
  returned["excess_return_" + str(i)] = returned[i] - rf

# COMMAND ----------

print(returned)
