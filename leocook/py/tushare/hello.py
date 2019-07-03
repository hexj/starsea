
## 获取上证指数的所以数据

# open 开盘
# high 最高
# close 收盘
# low 最低
# volume
# price_change
# p_change
# ma5 5日均线，该股票近5天的平均收盘价格
# ma10 10日均线
# ma20 20日均线
# v_ma5
# v_ma10
# v_ma20


import tushare as ts
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
# print(dir(ts))
# ts.get_hist_data('600848') #一次性获取全部日k线数据

# aa = ts.get_hist_data('600848')

print(ts.__version__)

d = ts.get_hist_data('000001',start='2016-01-01',end='2018-03-31')
print("colums:"+d.columns)
print(d)
# print(ts.get_hist_data('000001'))

