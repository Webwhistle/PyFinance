#!python3
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2015, 1, 1)
end = dt.datetime(2021,2,8)

df = web.DataReader('ITAB-B.ST', 'yahoo', start, end)

df.to_csv('itab.csv')
df = pd.read_csv('itab.csv', parse_dates = True, index_col=0)

df['100ma'] = df['Adj Close'].rolling(window=100).mean()
df.dropna(inplace=True)

print(df.tail())

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)

ax1.set_title("ITAB")
ax1.set_ylabel("SEK")
ax2.set_ylabel("Volym")

ax1.plot(df.index, df['Adj Close'], label ='Adj Close')
ax1.plot(df.index, df['100ma'], label = '100ma')
ax2.bar(df.index, df['Volume'])

plt.legend(loc='best')
ax1.legend()

plt.show()
