#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as ds

mu = 0.1 #上证年化率
Std = 0.2 #年化波动率
dt = 1/252. #每天
total_days = 10 #天数
init_price=99.98 #初始价格

def Simulation_StockPrice(S0, mu, Std, dt):
    S1 = S0 * np.exp((mu - 0.5 *Std**2)*dt + Std*np.sqrt(dt)*np.random.standard_normal())
    return S1

def dinge(prices):
    t=0.0
    for price in prices:
      t=t+1/price
    return len(prices)/t

def dingliang(prices):
    t=0.0
    for price in prices:
      t=t+price
    return t/len(prices)

if __name__ == "__main__":
    stat=[]
    for days in range(1,total_days):
        price = init_price
        price_list=[price]
        for d in range(1,days):
          price=Simulation_StockPrice(price,mu,Std,dt)
          price_list.append(price)
        stat.append([days,dinge(price_list)/dingliang(price_list)])
    rs=ds.DataFrame(stat).set_index(0)
    print(rs)
    rs[1].to_json('../data/random.json')







