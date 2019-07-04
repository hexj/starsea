
import pandas as pd
import numpy as np

# step1:生成随机数字典

# 生成随机数数组


# 把数组拼接成字典，key是date

# 天数
days = 5

# 数据条数
recodes = 100

# 列
columns = pd.date_range('20190705', periods=days)

#print(columns)

# 随机矩阵
c = np.random.randint(100, 200, (recodes, days))

#print(c)

# 矩阵转df
pdd = pd.DataFrame(c, columns=columns)

print(pdd)

