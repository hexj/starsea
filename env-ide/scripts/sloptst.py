# import modin.pandas as pd
import pandas as pd
import random
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

def has_none(values):
    for e in values:
        if e is None:
            return True
    return False

def average(values):
    count = len(values)
    assert count != 0
    s = sum(values)
    return s / float(count)

def slope(values, n):
    result = []
    for i, e in enumerate(values):
        if i < n-1:
            result.append(None)
            continue
        window = values[i-n+1:i+1]
        if has_none(window):
            result.append(None)
            continue
        xys = [(x, y) for x, y in enumerate(window)]
        xs = [x for x, y in xys]
        ys = [y for x, y in xys]
        a = sum([x*y for x, y in xys])
        b = n * average(xs) * average(ys)
        c = sum([x**2 for x in xs])
        r = (a-b)/(c-n*average(xs)**2)
        result.append(r)
    return result

def myslope(df, column_name, n):
    sta = stats.linregress(x, y)
    m = sta.slope
    np.polyfit
    pass

def print_type_sum(x):
    # print(type(x), x.shape)
    print(x)
    return x.sum()
def main():
    # 随机长度
    # nday = random.randint(10, 1000)  # 交易天数 通常在四年以内
    nday = 55
    minpi, maxpi = 2, 100  # 价格最小最大值
    # 随机矩阵 n 行 1 列
    rdarr = np.random.randint(minpi, maxpi, size=(nday,))
    df = pd.DataFrame(rdarr, columns=['price'])
    print(pd.Series(df['price']).rolling(3).sum())
    print(df.price.rolling(3,center=True).apply(print_type_sum))
    print(df.quantile(.3))
    slopes = df.apply(lambda x: np.polyfit(df.index, x, 1)[0])
    print(slopes)
    # def sslop(df,n):
    #     return df.apply(lambda y: {df.index, y})
    print(rdarr)
    slp = slope(rdarr,21)
    print(slp)
    df.insert(df.shape[1], 'slop', slp)
    # print(df)
    df.plot()
    plt.show()


def _time_analyze_(func):
    import time
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
