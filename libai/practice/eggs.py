#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bottle import route, run
from bottle import template,static_file


import random

number = 1000  # 一共2000天
max = 75  # 单价最大值
min = 25  # 单价最小值
cost = 500.0  # 定价的费用
amount = 50.0  # 定量的数量

#每天价格(动态)集合
priceList=[]
#定额成本集合
costPriceList=[]
#定量成本集合
amountPriceList=[]
daynumber=[]


def initList():


    # 固定价格的总份数
    totalCostAmount = 0

    # 固定份额的总价
    totalAmountCost = 0
    # 固定份额的总份数

    totalCostCost=0

    for i in range(1,number):
        # 固定价格的总价
        totalCostCost = cost * i

        totalAmountAmount = amount * i

        # 产生某天的价格(随机数)
        price = getRandom()
        priceList.append(price)
        #print("第" + str(i) + "天的单价是：" + str(price))
        # 计算固定价格的总份数
        totalCostAmount += cost / price;
        # 计算固定份额的总价
        totalAmountCost += amount * price;

        #print("固定总价的总分数：" + str(totalCostAmount))
        #print("固定份数的总价：" + str(totalAmountCost))

        costPrice = totalCostCost / totalCostAmount;
        amountPrice = totalAmountCost / totalAmountAmount;

        costPriceList.append(costPrice)
        amountPriceList.append(amountPrice)
        daynumber.append('第'+str(i)+'天')

        #print("定价的单价为：" + str(costPrice))
        #print("定量的单价为：" + str(amountPrice))
        #print("*****************")

    print(priceList)
    print(costPriceList)
    print(amountPriceList)
#    costPrice = totalCostCost / totalCostAmount;
#    amountPrice = totalAmountCost / totalAmountAmount;




def getRandom():
    return random.randint(min, max)


#定义图片路径
assets_path = './assets'

@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)
@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

@route('/hello')
def hello():
    return 'hello world'

@route('/')
def index():
    initList()
    strpriceList=priceList.__str__()
    strcostPriceList= costPriceList.__str__()
    # 定量成本集合
    stramountPriceList=amountPriceList.__str__()
    strdaynumber=daynumber.__str__()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print('strpriceList=',strpriceList)
    print('strcostPriceList',strcostPriceList)
    print('stramountPriceList',stramountPriceList)
    #print('strdaynumber',strdaynumber)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    return ''' <!DOCTYPE html>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="/assets/echarts.min.js"></script>
</head>
<body>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main" style="width: 1000px;height:800px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '定额定量定投对比图'
            },
            legend: {
                data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
            },
            xAxis: {
                type:'category',
                data : '''+strdaynumber +'''
            },
            yAxis: {
                type:'value'
            },
            series: [
            {
                name: '当天随机价格',
                type: 'line',
                smooth: true,
                data: '''+strpriceList+'''
            },
            {
                name:'固定总价成本',
                type:'line',
                smooth: true,
                data:'''+strcostPriceList+'''
            },
            {
                name:'固定总额成本',
                type:'line',
                smooth: true,
                data:'''+stramountPriceList+'''
            }
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>
</html> '''

run(host='localhost',port=8080)


