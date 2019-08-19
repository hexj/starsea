# -*- coding: utf-8 -*-
'''
定投场景下，定额和定量的比较
'''
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib

'''固定份额
假设定投n天，根据数学公式的推导，固定份额的平均价格为  (p1+p2+..+pn)/n
:params n: 天数
'''
def fixedAmt(n, seed = 10):
  prices = generateRandom(n, seed)
  result = 0.0
  final_result = np.sum(prices) / n
  return round(final_result, 3)

'''固定金额
假设定投n天，根据数学公式的推导，固定金额的平均价格为  n/(1/p1 + 1/p2 + 1/p3 + ... +1/pn)
:params n: 天数
'''
def fixedMoney(n, seed = 10):
  prices = generateRandom(n, seed)
  result = np.sum(1/prices)
  final_result = n/result
  return round(final_result, 3)

'''
调用numpy生成固定价格范围的内的随机数
'''
def generateRandom(n, seed):
  np.random.seed(seed)
  return (np.random.uniform(10., 6., size = n))

'''
显示统计图
:param years: 定投年数
:param fixed_amt_avg_price: 固定金数量投算出来的均价
:param fixed_money_avg_price: 固定金额计算出来的均价
'''
def showStatistic(years, fixed_amt_avg_prices, fixed_money_avg_prices):
  x = range(len(fixed_amt_avg_prices))
  rects1 = plt.bar(x=x, height=fixed_amt_avg_prices, width=0.4, alpha=0.8, color='red', label="FIXED_AMOUNT")
  rects2 = plt.bar(x=[i + 0.4 for i in x], height=fixed_money_avg_prices, width=0.4, color='green', label="FIXED MONEY")
  # y轴取值范围
  plt.ylim(0, 10)
  plt.ylabel("Avg. Cost Price")
  plt.xticks([index + 0.2 for index in x], years)
  plt.xlabel("Year")
  plt.title(f"Average Cost Price for {len(years)} years, Price Range: 6-10")
  # 设置题注
  plt.legend()
  # 编辑文本
  for rect in rects1:
      height = rect.get_height()
      plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
  for rect in rects2:
      height = rect.get_height()
      plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
  plt.show()

def log(s):
  print(s)
  pass

if __name__  == '__main__':
  fixed_amt_avg_prices = []
  fixed_money_avg_prices = []
  years = list(range(1, 21))
  for i in years:
    # 当前时间的秒数
    t = time.time()
    # 当前时间的秒数+1做为这次循环的种子数，同一次计算不同的定投方式中所使用的数据样本是一样的
    seed = int(round(t + i))
    log(f'the seed is : {seed}')

    # 暂定每年250个交易日
    avgPrice1 = fixedAmt(i * 250, seed)
    fixed_amt_avg_prices.append(avgPrice1)
    avgPrice2 = fixedMoney(i * 250, seed)
    fixed_money_avg_prices.append(avgPrice2)

  log(fixed_amt_avg_prices)
  log(fixed_money_avg_prices)
  showStatistic(years, fixed_amt_avg_prices, fixed_money_avg_prices)

  
