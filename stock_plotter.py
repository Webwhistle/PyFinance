#!python3
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np

def stock_scraper(stock, horizon = 'Short'):
    """
    Collects and samples existing financial data over a chosen stock and time
    period. Plots with a few TA-parameters.
    """
    name = stock
    if horizon == 'Long':
        start = dt.datetime(2016, 1, 1)
        end = dt.datetime(2021,2,8)
    else:
        start = dt.datetime(2019, 7, 1)
        end = dt.datetime(2021,2,8)

    df = web.DataReader(stock, 'yahoo', start, end)

    df.to_csv(str(name)+'.csv')
    df = pd.read_csv(str(name)+'.csv', parse_dates = True, index_col=0)

    df['5ma'] = df['Adj Close'].rolling(window=5).mean()
    df['20ma'] = df['Adj Close'].rolling(window=20).mean()
    df['50ma'] = df['Adj Close'].rolling(window=50).mean()
    df['100ma'] = df['Adj Close'].rolling(window=100).mean()
    df['200ma'] = df['Adj Close'].rolling(window=200).mean()
    df.dropna(inplace=True)

    plt.figure(figsize=(8,8))

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)

    ax1.set_title(str(name))
    ax1.set_ylabel("SEK")
    ax2.set_ylabel("Volym")

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1, label = str(name))
    x = df.index
    close = df['Adj Close']
    plt.title(str(name))

    if horizon == 'Long':
        f = df['200ma']
        g = df['50ma']
        plt.plot(x, close, label = 'Adj Close', color = 'steelblue')
        plt.plot(x, f, '-', label = '200ma', color = 'darkkhaki')
        plt.plot(x, g, '-', label = '50ma', color = 'darkorange')
    else:
        f = df['5ma']
        g = df['20ma']
        plt.plot(x, close, label = 'Adj Close', color = 'steelblue')
        plt.plot(x, g, '-', label = '20ma', color = 'darkkhaki')
        plt.plot(x, f, '-', label = '5ma', color = 'darkorange')

    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()
    #plt.plot(x[idx], f[idx], 'o', color = 'purple', label = 'ma-crossover')
    plt.plot(x[idx], close[idx], '-', color =  'seagreen', label = 'Crossover Adj Close Result')

    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)
    plt.bar(x, df['Volume'], color = 'steelblue')

    plt.legend(loc='best')
    ax1.legend()

    plt.show()

stora_bolag = ['SWMA.ST', 'AZN', 'ATCO-B.ST', 'ERIC-B.ST', 'SKF-B.ST', 'SEB-A.ST']

stock_scraper('ITAB-B.ST')
