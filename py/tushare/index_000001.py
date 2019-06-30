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

pro = ts.pro_api()

metric = pro.index_daily(ts_code='000001.SH')
print("metric colums:"+metric.columns)
print(metric)

metric.to_csv("csv/index_000001.csv")

