#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import pandas as pd
import numpy as np
import time

def slope(y, x=None): # list or array like
    n = len(y)
    if(x is None): x = np.arange(n)
    y = np.asarray(y)
    if (n < 50) :
        return ((n*sum(x*y)) - (sum(x)*sum(y))) / (n*(sum(x**2))-(sum(x)**2))
    else:
        ssxm, ssxym, ssyxm, ssym = np.cov(x, y, bias=True).flat
        return ssxym / ssxm


def _get_valid_index(values, start_index=0, n = None):
    if(start_index < 0):
        start_index = n + start_index
    if(start_index == 0):
        for i, val in enumerate(values):
            if val is not None: return i
    return start_index


def ema(series, n, colname='close', start_index=0):  # 起始值为0:n-1的last
    start_index = _get_valid_index(series.to_numpy(), start_index, n)
    emacol = series.copy()
    if(start_index > 0):
        lep = start_index - 1
        emacol[:lep] = None
    return emacol.ewm(span=n, adjust=False).mean()


def cross(A, B):
    iscross = A.iloc[-2] < B.iloc[-2] and A.iloc[-1] > B.iloc[-1]
    return iscross

def plot(df, col=1, row=1):
    from matplotlib import pyplot as plt
    df.plot() 
    plt.show()

def feedtsdata():
    import datetime
    import tushare as ts
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    df = ts.get_k_data('600050', start='2019-09-01', end=today)
    return df

today = datetime.datetime.now().strftime('%Y-%m-%d')
def feedtdxdata():
    h5file = "dayochlv.h5"
    h5key = 'dayochlv'
    # dfr = pd.read_hdf(h5file, 'dayochlv', where='')
    store = pd.HDFStore(h5file)
    nrows = store.get_storer('df').nrows
    chunksize=100
    for i in xrange(nrows//chunksize + 1):
        chunk = store.select(h5key, start=i * chunksize, stop=(i+1)*chunksize)
    store.close()
    return df

def randomdata():
    nday = 50  # 交易天数 通常在四年以内
    minpi, maxpi = 2, 100  # 价格最小最大值
    rdarr = np.random.randint(minpi, maxpi, size=(nday,))  # 随机矩阵 n 行 1 列
    colname = "Close"
    df = pd.DataFrame(rdarr, columns=[colname])
    return df

def slop_test():
    df = feedtsdata()
    slop_strategy(df, colname='close')

def difftest():
    df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6], 'b': [111, 100, 20, 30, 50, 8], 'c': [None, 4, 90, 16, 25, 36]})
    df['diff']  = df['c']-df['b']
    df['cross'] = np.sign(df['diff'])
    df['sign'] = np.sign(df['cross'].shift(1) - df['cross'])
    print(df)

def slop_strategy(df, colname='close'):
    # VAR1: = EMA(C, 2)
    # VAR2: = EMA(SLOPE(C, 21)*20+C, 42)
    buy_n, slope_n, sellp_n, sell_n = 2, 21, 20, 42
    bline, sline = 'buyline', 'sellline'
    df['slope'] = df[colname].rolling(slope_n).apply(slope, raw=True)
    df['sellp'] = df['slope'] * sellp_n + df[colname]
    df[bline] = ema(df[colname], buy_n)
    df[sline] = ema(df['sellp'], sell_n)
    df['diff'] = df[sline] - df[bline]
    df['cross'] = np.sign(df['diff'])
    df['sign'] = np.sign(df['cross'].shift(1) - df['cross'])
    # df['sign'] = df['cross'].rolling(2).apply(cross_val, raw=True)
    # print(np.sum(df['cross'])-1)
    rst = df[[colname, bline, sline,'diff','sign']]
    df[['close','sign']].rolling(1).apply(lambda x: print(x))
    print(df)
    # plot(rst)
    return df

def main():
    difftest()
    # slop_test()

def _time_analyze_(func):
    t1_start = time.perf_counter()
    func()
    t1_stop = time.perf_counter()
    print("Elapsed time: %s s" % (t1_stop - t1_start))


if __name__ == '__main__':
    _time_analyze_(main)

# VAR1: = EMA(C, 2)
# VAR2: = EMA(SLOPE(C, 21)*20+C, 42)
# VAR3: = CROSS(VAR1, VAR2)
# VAR4: = CROSS(VAR2, VAR1)
