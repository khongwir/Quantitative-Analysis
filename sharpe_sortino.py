import yfinance as yf
import pandas as pd
import numpy as np

tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR
    
def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    vol = df["return"].std() * np.sqrt(252)
    return vol

def sharpe(DF, rf):
    "function to calculate Sharpe Ratio of a trading strategy"
    df = DF.copy()
    return (CAGR(df) - rf)/volatility(df)

def sortino(DF, rf):
    "function to calculate Sortino Ratio of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    neg_return = np.where(df["return"]>0,0,df["return"])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252)
    return (CAGR(df) - rf)/neg_vol

for ticker in ohlcv_data:
    print("Sharpe of {} = {}".format(ticker,sharpe(ohlcv_data[ticker],0.03)))
    print("Sortino of {} = {}".format(ticker,sortino(ohlcv_data[ticker],0.03)))
    
    
    
    