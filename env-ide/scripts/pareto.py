#-*- coding: utf-8 -*-
#-- file pareto.py --
#菜品盈利数据 帕累托图
from __future__ import print_function
import matplotlib.pyplot as plt  # 导入图像库
import pandas as pd
import os

#初始化参数
dish_profit_file = '../data/catering_dish_profit.xlsx'  # 餐饮菜品盈利数据
dish_profit = os.path.abspath(os.path.join(os.getcwd(), dish_profit_file))
data = pd.read_excel(dish_profit, index_col=u'菜品名')
data = data[u'盈利'].copy()
data.sort_values(ascending=False)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.figure()
data.plot(kind='bar')
plt.ylabel(u'盈利（元）')
p = 1.0*data.cumsum()/data.sum()
p.plot(color='r', secondary_y=True, style='-o', linewidth=1)

# xy设置箭头尖的坐标
# xytext设置注释内容显示的起始位置
# arrowprops 用来设置箭头

plt.annotate(format(p[6], '20%'), xy=(6, p[6]), xytext=(6*0.9, p[6]*0.9),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#添加注释，即85%处的标记。这里包括了指定箭头样式。
#format(p[6], '20%')  20%为箭头尾部的线的长度
#connectionstyle="arc3,rad=.2" 指的是指向箭头的弯曲程度
plt.ylabel(u'盈利（比例）')
plt.show()
