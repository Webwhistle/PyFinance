#!python3
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np

def stock_scraper(stock = "^OMX"):
    """
    Collects and samples existing financial data over a chosen stock and time
    period. Plots with MA-crossovers for either short och long term time interval.
    """
    name = "OMX30"
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2021,2,14)

    df = web.DataReader(stock, 'yahoo', start, end)

    df.to_csv('large_cap.csv')
    df = pd.read_csv('large_cap.csv', parse_dates = True, index_col=0)

    df['5ma'] = df['Adj Close'].rolling(window=5).mean()
    df['20ma'] = df['Adj Close'].rolling(window=20).mean()
    df['50ma'] = df['Adj Close'].rolling(window=50).mean()
    df['100ma'] = df['Adj Close'].rolling(window=100).mean() #Not used
    df['200ma'] = df['Adj Close'].rolling(window=200).mean()
    df.dropna(inplace=True)

    x = df.index
    close = df['Adj Close']

    f = df['50ma']
    f_label = "50ma"
    g = df['200ma']
    g_label = "200ma"

    #Points of ma-crossovers
    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()

    #Related prices to ma-crossovers (cp = crossover price)
    cp = close[idx].values.tolist()

    #Price differences between ma-crossovers value
    absolute_difference = [(cp[i] - cp[i+1]) for i in range(len(cp)-1)]

    """ Plots adjusted close price, two different MA:s and their crossover
        with volume. """

    plt.figure(figsize=(8,8))

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)

    ax1.set_title(str(name))
    ax1.set_ylabel("SEK")
    ax2.set_ylabel("Volym")

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1, label = str(name))
    plt.title(str(name))
    plt.plot(x, close, label = 'Adj Close', color = 'steelblue')
    plt.plot(x, f, '-', label = f_label, color = 'darkorange')
    plt.plot(x, g, '-', label = g_label, color = 'darkkhaki')

    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)
    plt.bar(x, df['Volume'], color = 'steelblue')

    ax1.legend(loc='best')

    plt.show()

stock_scraper()
