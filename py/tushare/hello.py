
## 获取上证指数的所以数据

import tushare as ts
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
# print(dir(ts))
# ts.get_hist_data('600848') #一次性获取全部日k线数据

# aa = ts.get_hist_data('600848')


print(ts.get_hist_data('000001',start='2016-01-01',end='2018-03-31'))
# print(ts.get_hist_data('000001'))




