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
    period. Plots with MA-crossovers for either short och long term time interval.
    """
    name = stock
    if horizon == 'Long':
        start = dt.datetime(2016, 1, 1)
        end = dt.datetime(2021,2,8)
    else:
        start = dt.datetime(2019, 7, 1)
        end = dt.datetime(2021,2,8)

    df = web.DataReader(stock, 'yahoo', start, end)

    df.to_csv('stock_data.csv')
    df = pd.read_csv('stock_data.csv', parse_dates = True, index_col=0)

    df['5ma'] = df['Adj Close'].rolling(window=5).mean()
    df['20ma'] = df['Adj Close'].rolling(window=20).mean()
    df['50ma'] = df['Adj Close'].rolling(window=50).mean()
    df['100ma'] = df['Adj Close'].rolling(window=100).mean() #Not used
    df['200ma'] = df['Adj Close'].rolling(window=200).mean()
    df.dropna(inplace=True)

    x = df.index
    close = df['Adj Close']

    if horizon == 'Long':
        f = df['50ma']
        f_label = "50ma"
        g = df['200ma']
        g_label = "200ma"
    else:
        f = df['5ma']
        f_label = "5ma"
        g = df['20ma']
        g_label = "20ma"

    #Points of ma-crossovers
    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()

    #Related prices to ma-crossovers (cp = crossover price)
    cp = close[idx].values.tolist()

    #Price differences between ma-crossovers value
    absolute_difference = [(cp[i] - cp[i+1]) for i in range(len(cp)-1)]

    if f[0] > g[0]:
        """ Checks beginning position of MA """
        print("Short ma over long " + str(stock))
        for i in range(len(absolute_difference)):
            if i%2 != 0:
                absolute_difference[i] = -(absolute_difference[i])
        period_result = sum(absolute_difference)
        #print('Period result: ' + str(period_result))
    else:
        print("Long ma over short " + str(stock))
        for i in range(len(absolute_difference)):
            if i%2 == 0:
                absolute_difference[i] = -(absolute_difference[i])
        period_result = sum(absolute_difference)
        #print('Period result: ' + str(period_result))

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

    plt.plot(x[idx], f[idx], 'o', color = 'purple', label = 'ma-crossover')
    plt.plot(x[idx], close[idx], '-', color =  'seagreen', label = 'Crossover Adj Close Result')

    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)
    plt.bar(x, df['Volume'], color = 'steelblue')

    ax1.legend(loc='best')

    plt.show()

    # Returns result based on crossover trading and opening price
    return period_result, close[0]

bolag = ['SWMA.ST', 'AZN', 'ATCO-B.ST', 'ERIC-B.ST', 'SKF-B.ST',
'SEB-A.ST', 'ITAB-B.ST', 'VOLV-B.ST', 'HM-B.ST', 'ALFA.ST', 'ASSA-B.ST',
'BOL.ST', 'ELUX-B.ST', 'FING-B.ST', 'GETI-B.ST', 'KINV-B.ST', 'NDA-SE.ST',
'SAND.ST','SECU-B.ST','SKA-B.ST','SSAB-A.ST','SWED-A.ST',
'SCA-B.ST','SHB-B.ST', 'TEL2-B.ST', 'TELIA.ST']

assert len(bolag) == len(list(set(bolag)))

def plot_companies(how_many = len(bolag), horizon = 'Short'):
    """ Summarizes several companies based on above list. """
    results = []
    total_price = 0
    for i in bolag[:how_many]:
        result, price = stock_scraper(i,horizon)
        results.append(result)
        total_price += price
    return results, total_price

"""
results, total_price = plot_companies()
negative = 0
for i in results:
    if i < 0:
        negative +=1

print('Losers: ' + str(negative))
print('Winners: ' + str(len(results)-negative))
print('Total value ' + str(total_price))
print('Totalt result: ' + str(sum(results)))
"""

stock_scraper('ANOT.ST', 'Long')
stock_scraper('ANOT.ST', 'Short')
