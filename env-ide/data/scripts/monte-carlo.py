#!/usr/bin/env python
# -*- coding: utf-8 -*-
########-----展现平均持有单价变化-----########
import pandas as pd
import numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt

def eachtime():
    # 随机长度
    nday = random.randint(10,1000) #交易天数 通常在四年以内
    minpi,maxpi= 2,100 #价格最小最大值
    # 随机矩阵 n 行 1 列
    rdarr = np.random.randint(minpi, maxpi, size=(nday,))
    df = pd.DataFrame(rdarr, columns=['price'])
    pd.set_option('precision', 12) #小数点精度
    
    #### 定额方式 ####
    df['amt_p-rec'] = 1.0/df['price'] # 价格倒数 p-rec
    df['amt_sum-vol'] = df['amt_p-rec'].cumsum() #定额总量，价格倒数累加求和
    df['定额单价'] = (df.index + 1)/df['amt_sum-vol'] #定额平均单价 = 总价/总量
    
    #### 定量方式 ####
    df['vol_sum-vol'] = df['price'].cumsum() # 定量总价
    df['定量单价'] = df['vol_sum-vol']/(df.index + 1) #定量平均单价 = 总价/总量
    
    df['量额比'] = df['定量单价']/df['定额单价'] 
    rstdf = df[['price','定额单价','定量单价','量额比']]
    print(nday) 
    rstdf.plot()
    plt.show()
    print(rstdf.head())

def init_font():
    font_name = 'SimHei' 
    plt.rcParams['font.family'] = font_name #用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.rcParams['font.sans-serif'].append(font_name)
    plt.rcParams['figure.figsize'] = 16, 8
    import matplotlib.font_manager
    matplotlib.font_manager._rebuild()
    print(matplotlib.font_manager.findfont(font_name))


def main(): 
    init_font()
    testcnt = 2 #000
    for i in range(testcnt):
        eachtime() #算单条
    print("-end-")

if __name__ == '__main__':
    main()