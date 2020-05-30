#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from echarts import Echart, Legend, Bar, Axis

chart = Echart('GDP', 'This is a fake chart')
chart.use(Bar('China', [2, 3, 4, 5]))
chart.use(Legend(['GDP']))
chart.use(Axis('category', 'bottom', data=['Nov', 'Dec', 'Jan', 'Feb']))
chart.plot()
# print(chart.json)
