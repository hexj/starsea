
import pandas as pd
import numpy as np

# step1:生成随机数字典

# 生成随机数数组


# 把数组拼接成字典，key是date

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#pd.set_option('display.width', None)

# 天数
days = 50

# 数据条数
recodes = 100000

# 定量
buckNum = 100

# 定额
buckPrice=100000

# 列
columns = pd.date_range('20190705', periods=days).map(lambda x: x.strftime('%Y%m%d'))

#print(columns)

# 随机矩阵
c = np.random.randint(100, 2000, (recodes, days))

# print(c)

# 矩阵转df
pdd = pd.DataFrame(c, columns=columns)
print(pdd)

print('----------------------------------------------------------------')

def process(row):
    sum = 0
    sum_reciprocal = 0
    lastIndex = len(columns) - 1
    for index in range(lastIndex):
        sum = sum + row[index]
        sum_reciprocal = sum_reciprocal + 1.0 / row[index]

    # 定量（盈利率）
    a = row[lastIndex] * lastIndex / sum - 1

    # 定量（平均成本单价）
    b = sum / lastIndex

    # 定额（盈利率）
    c = row[lastIndex] * sum_reciprocal / lastIndex - 1

    # 定额（平均成本单价）
    d = lastIndex / sum_reciprocal

    return pd.Series([
        a,
        b,
        c,
        d,
        a - c,
        b - d
    ])



# 定量（盈利率）
def dingliang(row):
    sum = 0.0
    lastIndex = len(columns) - 1
    for index in range(lastIndex):
        sum = sum + row[index]
    return row[lastIndex] * lastIndex / sum - 1


# 定量（平均成本单价）
def dingliang_price(row):
    sum = 0.0
    lastIndex = len(columns) - 1
    for index in range(lastIndex):
        sum = sum + row[index]
    return sum / lastIndex


# 定额（盈利率）
def dinge(row):
    sum = 0.0
    lastIndex = len(columns) - 1
    for index in range(len(columns) - 1):
        sum = sum + 1.0 / row[index]
    return row[lastIndex] * sum / lastIndex - 1


# 定额（平均成本单价）
def dinge_price(row):
    sum = 0.0
    lastIndex = len(columns) - 1
    for index in range(len(columns) - 1):
        sum = sum + 1 / row[index]
    return lastIndex / sum




# 定量（持有股数）、定量（持有股数）；定额（平均单价成本）、定量（平均单价成本）；定额（盈利率）、定量（盈利率）；定额（盈利额）、定量（盈利额）

# 定额（盈利额）、定量（盈利额）
# 最后一天是成交价
pdd[['定量（盈利率）','定量（平均成本单价）','定额（盈利率）','定额（平均成本单价）', '定量-定额（盈利率）','定量-定额（平均成本单价）']] = pdd.apply(lambda row: process(row), axis=1)

print(pdd)

print('----------------------------------------------------------------')

print('定量（盈利率） > 定额（盈利率）')
print(str(pdd[pdd['定量-定额（盈利率）'] > 0]['定量-定额（盈利率）'].count()/recodes * 100) + '%\n' )

print('定量（盈利率） > 0')
print(str(pdd[pdd['定量（盈利率）'] > 0]['定量（盈利率）'].count()/recodes * 100) + '%\n' )

print('定额（盈利率） > 0')
print(str(pdd[pdd['定额（盈利率）'] > 0]['定额（盈利率）'].count()/recodes * 100) + '%\n' )

print('定量（平均成本单价） > 定额（平均成本单价）')
print(str(pdd[pdd['定量-定额（平均成本单价）'] > 0]['定量-定额（平均成本单价）'].count()/recodes * 100) + '%\n' )
