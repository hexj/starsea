#!/usr/bin/python
# -*- coding: utf-8 -*-
import tushare as ts
#获取A股代码
codes=ts.get_stock_basics().reset_index()['code']
print(codes)
