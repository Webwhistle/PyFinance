#!python3
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

def stock_scraper(start_time, end_time, stock, name):
    start = start_time
    end = end_time
    stock = stock

    df = web.DataReader(stock, 'yahoo', start, end)

    df.to_csv(str(name)+'.csv')
    df = pd.read_csv(str(name)+'.csv', parse_dates = True, index_col=0)

    df['100ma'] = df['Adj Close'].rolling(window=100).mean()
    df.dropna(inplace=True)

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)

    ax1.set_title(str(stock))
    ax1.set_ylabel("SEK")
    ax2.set_ylabel("Volym")

    ax1.plot(df.index, df['Adj Close'], label ='Adj Close')
    ax1.plot(df.index, df['100ma'], label = '100ma')
    ax2.bar(df.index, df['Volume'])

    plt.legend(loc='best')
    ax1.legend()

    plt.show()

start = dt.datetime(1980, 1, 1)
end = dt.datetime(2021,2,8)
sts = 'AAPL'
st = 'apple'

stock_scraper(start, end, sts, st)
