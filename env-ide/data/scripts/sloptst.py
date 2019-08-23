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

def myslope(df,n):
    sta = stats.linregress(x, y)
    m = sta.slope
    pass
# 随机长度
# nday = random.randint(10, 1000)  # 交易天数 通常在四年以内
nday = 30
minpi, maxpi = 2, 100  # 价格最小最大值
# 随机矩阵 n 行 1 列
rdarr = np.random.randint(minpi, maxpi, size=(nday,))
df = pd.DataFrame(rdarr, columns=['price'])

# slopes = df.apply(lambda x: np.polyfit(df.index, x, 1)[0])
# def sslop(df,n):
#     slopes = df.apply(lambda y: {df.index, y} )
slp = slope(rdarr,21)
print(slp)
# df.plot()
# plt.show()

# VAR1: = EMA(C, 2)
# VAR2: = EMA(SLOPE(C, 21)*20+C, 42)
# VAR3: = CROSS(VAR1, VAR2)
# VAR4: = CROSS(VAR2, VAR1)
