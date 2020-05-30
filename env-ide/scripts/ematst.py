#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import random
import numpy as np
import time

def _time_analyze_(func):
    def timed(*args, **kwargs):
        t1_start = time.time()
        rst = func(*args, **kwargs)
        t1_stop = time.time()
        elapse = t1_stop - t1_start
        strtmp = "{0} elapse {1} ms "
        print(strtmp.format(func.__name__, elapse*1000.0))
        return rst
    return timed


# @_time_analyze_
def _get_valid_index(values, start_index=0, n=None):
    if(start_index < 0): start_index = n + start_index
    if(start_index == 0):
        for i, val in enumerate(values):
            if val is not None: return i
    return start_index


@_time_analyze_
def expma02(df, n=20, start_index=0):  # start_index=n-1
    # print(df.columns.values)
    start_index = _get_valid_index(df.to_numpy(), start_index, n)
    if(start_index == 0):
        return df.ewm(span=n, adjust=False).mean()
    start = pd.Series(np.nan, index=range(start_index+1))
    start.iat[start_index] = df.iat[start_index]
    return pd.concat([start, df[start_index+1:]]).ewm(span=n, adjust=False).mean()


@_time_analyze_
def expma002_(df, n=20, start_index=0):  # 起始值为0:n-1的last
    start_index = _get_valid_index(df.to_numpy(), start_index, n)
    ema = df.copy()
    if(start_index > 0):
        ema[:start_index - 1] = None
    return ema.ewm(span=n, adjust=False).mean()

@_time_analyze_
def expma002(df, n=20, start_index=0):  # 起始值为0:n-1的last
    start_index = _get_valid_index(df.to_numpy(), start_index, n)
    ema = df.copy()
    if(start_index > 0):
        lep = start_index - 1
        ema[:lep] = None
    return ema.ewm(span=n, adjust=False).mean()

@_time_analyze_
def expma2(df, n=20):# 起始值为0:n-1的sma
    sma = df[:n].rolling(window=n, min_periods=n).mean() #sma as df[n-1]
    return pd.concat([sma, df[n:]]).ewm(span=n, adjust=False).mean()


@_time_analyze_
def expma1(values, n=20):
    length_of_df = len(values)
    alpha = 2.0/(n + 1.0)
    ema = pd.Series(np.nan, index=range(0, length_of_df))
    ema.iat[n-1] = values[0:n].mean() #initial_sma
    for i in range(n, length_of_df):
        ema.iat[i] = values.iat[i] * alpha + (1-alpha) * ema.iat[i-1]
    return ema


@_time_analyze_
def expma_pascal(values, n=10, start_index=0):
    length_of_df = len(values)
    initial_val = values[start_index].mean()
    # print(initial_val)
    ema = pd.Series(np.nan, index=range(0, length_of_df))
    ema.iat[start_index] = initial_val
    for i in range(start_index+1, length_of_df):
        ema.iat[i] = (2*values.iat[i] + (n-1)*ema.iat[i-1])/(n+1)
    return ema


@_time_analyze_
def expma0(values, n=20):
    result = []
    alpha = 2.0 / (n+1.0)
    for i, e in enumerate(values):
        if i < n-1:
            result.append(None)
            continue
        window = values[i-n+1:i+1]
        if None in window:
            result.append(None)
            continue
        last = result[-1]
        if last is None: last = e
        rst = e*alpha + (1-alpha)*last
        result.append(rst)
    return result


@_time_analyze_
def get_valid_index(values):
    start_index = 0
    for i, val in enumerate(values):
        if val is not None:
            start_index = i
            return i
    return start_index


@_time_analyze_
def tdx_xn01(values, n, start_index=0):
    alpha = 2.0/(n + 1.0)
    dest = np.full(len(values), np.nan)
    if(start_index == 0):
        start_index = get_valid_index(values)
    dest[start_index] = values[start_index]
    for i, val in enumerate(values):
        if(i > start_index):
            # dest[i] = (2*val + (n-1)*dest[i-1] )/(n+1)
            dest[i] = val*alpha + (1-alpha)*dest[i-1]
    return dest


@_time_analyze_
def ewm_adjf(df, n=20, start_index = 0):  # start_index=n-1
    return df.ewm(span=n, adjust=False).mean()

# @_time_analyze_
def ewma(n=20):  # 对比不同的ema计算方法 
    print("-----n=%s" % n)
    colname = "close"
    df = pd.DataFrame(rdarr, columns=[colname])
    # print(df[colname].to_numpy())
    # df['pct_sf'] = df.index.map(lambda x: df[colname].ix[:x].rank(pct=True)[x])
    if(len(df.index)<n ): 
        print("n bigger than df len: n=%s,len(df)=%s"%(n,len(df.index)))
        return None
    # df['0_ewm'] = expma0(df[colname].to_numpy(), n)
    # df['ewma_tdx_xn01'] = tdx_xn01(df[colname].to_numpy(), n, start_index=n-1)
    df['02_ewm_last'] = expma02(df[colname], n=n, start_index=n-1)
    df['002_ewm_last'] = expma002(df[colname], n=n, start_index=n-1)
    df['_002_ewm_last'] = expma002_(df[colname], n=n, start_index=n-1)
    # df['1_ewm'] = expma1(df[colname], n=n) #= df['2_ewm']
    # df['2_ewm_sma'] = expma2(df[colname], n=n)
    # df['ewm-adjf'] = ewm_adjf(df[colname], n=n)
    # df['ewma_pascal'] = expma_pascal(df[colname], n) # = df['ewm-adjf']
    # df['ewma_adjt'+str(n)] = df[colname].ewm(span=n).mean()
    # df['ewma_qa'+str(n)] = df[colname].ewm(span=n, min_periods=n - 1).mean()
    # df2 = df.reindex(index=df.index[::-1])
    # print(df[n-1:n+10].head())


@_time_analyze_
def plot(df):
    df.plot()
    from matplotlib import pyplot as plt
    plt.show()


# nday = random.randint(10, 1000)  # 随机长度
nday = 15500  # 交易天数 通常在四年以内
minpi, maxpi = 2, 100  # 价格最小最大值
# 随机矩阵 n 行 1 列
rdarr = np.random.randint(minpi, maxpi, size=(nday,))

@_time_analyze_
def main():
    arrs = [2, 10, 21, 30, 42, 50, 60, 80, 100, 120, 250, 250, 350, 500]
    for n in arrs : ewma(n)
    # ewma()

if __name__ == '__main__':
    # _time_analyze_(main)
    main()
