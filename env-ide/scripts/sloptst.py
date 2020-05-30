# import modin.pandas as pd
import pandas as pd
import random
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import pysnooper
import time

def sharpe():
    returns = [-0.999999, 1, 0.5]
    return_mean = np.mean(returns)  # 0.166667
    return_benchmark = 1.04 ** (1/250) - 1  # 0.0001568951593713397
    return_std = np.std(returns, ddof=1)  # 1.0408324392845372
    sharpe = (return_mean - return_benchmark) / return_std  # 0.15997782021003001
    print(return_mean, return_benchmark, return_std, sharpe)
    ## https://www.zhihu.com/question/27264526/answer/532397165

def slope_old(values, n):
    result = []
    for i, e in enumerate(values):
        if i < n-1:
            result.append(None)
            continue
        window = values[i-n+1:i+1]
        if None in window:
            result.append(None)
            continue
        # y = window
        xys = [(x, y) for x, y in enumerate(window)]
        xs = [x for x, y in xys]
        ys = [y for x, y in xys]
        a = sum([x*y for x, y in xys])
        b = n * xs.mean() * ys.mean()
        c = sum([x**2 for x in xs])
        r = (a-b)/(c-n*xs.mean()**2)
        result.append(r)
    return result

def average(values):
    return sum(values) / float(len(values))

def slope003(y):
    n = len(y)
    x = np.arange(n)
    a = sum(x*y)
    xsavg = average(x)
    yavg = average(y)
    b = n * xsavg * yavg
    c = sum(x**2)
    r = (a-b)/(c-n*xsavg**2)
    return r

def slope03(y):
    n = len(y)
    x = np.arange(n)
    a = sum(x*y)
    xsavg = np.mean(x)
    yavg = np.mean(y)
    b = n * xsavg * yavg
    c = sum(x**2)
    r = (a-b)/(c-n*xsavg**2)
    return r

def slope3(window):
    n = len(window)
    xys = [(x, y) for x, y in enumerate(window)]
    xs = [x for x, y in xys]
    ys = [y for x, y in xys]
    a = sum([x*y for x, y in xys])
    xsavg = np.mean(xs)
    b = n * xsavg * np.mean(ys)
    c = sum([x**2 for x in xs])
    r = (a-b)/(c-n*xsavg**2)
    return r

def slope2(y):
    n = len(y)
    x = np.arange(n)
    return ((n*sum(x*y)) - (sum(x)*sum(y))) / (n*(sum(x**2))-(sum(x)**2))

def slope1(y):
    x = np.arange(len(y))
    return stats.linregress(x, y)[0]

def slope0(y):
    x = np.arange(len(y))
    y = np.asarray(y)
    ssxm, ssxym, ssyxm, ssym = np.cov(x, y, bias=True).flat
    return ssxym / ssxm


# nday = random.randint(10, 1000)  # 随机长度
nday = 5500  # 交易天数 通常在四年以内
minpi, maxpi = 2, 100  # 价格最小最大值
# 随机矩阵 n 行 1 列
rdarr = np.random.randint(minpi, maxpi, size=(nday,))

# @pysnooper.snoop()
def myslope(n = 20):
    print("-----n=%s"%n)
    colname = 'price'
    df = pd.DataFrame(rdarr, columns=[colname])
    t0 = time.time()
    df['slope0'] = df[colname].rolling(n).apply(slope0, raw=True)
    t1 = time.time()
    # df['slope1'] = df[colname].rolling(n).apply(slope1, raw=True)
    t2 = time.time()
    df['slope2'] = df[colname].rolling(n).apply(slope2, raw=True)
    t3 = time.time()
    # df['slope3'] = df[colname].rolling(n).apply(slope3, raw=True)
    t03 = time.time()
    df['slope03'] = df[colname].rolling(n).apply(slope03, raw=True)
    t003 = time.time()
    # df['slope003'] = df[colname].rolling(n).apply(slope003, raw=True)
    te = time.time()
    # df['polyfit'] = df[colname].apply(lambda x: np.polyfit(df.index, x, 1)[0])
    # df.plot()
    # plt.show()
    # print(df.tail(2))
    print("slope0 {0}s".format(t1-t0))
    # print("slope1 {0}s".format(t2-t1))
    print("slope2 {0}s".format(t3-t2))
    # print("slope3 {0}s".format(t03-t3))
    print("slope03 {0}s".format(t003-t03))
    # print("slope003 {0}s".format(te-t003))
    pass


def main():
    for n in [2,10,21,30,42,50,60,80,100,120,250] :
        myslope(n)
    # print(df.quantile(.3))

def _time(func):
    t1_start = time.time()
    func()
    t1_stop = time.time()
    print("Elapsed time for {}: {} s".format( func.__name__, (t1_stop - t1_start)))


def timer(func):
    '''Function Level Timer via Decorator'''
    def timed(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        elapse = (end - start).total_seconds()
        print("Processing time for {} is: {} seconds".format(func.__name__, elapse))
        return result
    return timed

if __name__ == '__main__':
    _time(main)

# VAR1: = EMA(C, 2)
# VAR2: = EMA(SLOPE(C, 21)*20+C, 42)
# VAR3: = CROSS(VAR1, VAR2)
# VAR4: = CROSS(VAR2, VAR1)
