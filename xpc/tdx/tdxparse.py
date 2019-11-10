#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import struct
import datetime
from bottle import route, run
from bottle import template,static_file


@route( "/hello")
def application( ):
    return "hello"

# 查指定code的数据
def stock_query(filepath, filename):

    print("read file start, filename:" + filename)
    if filename == ".DS_S":
        print("ignore")
    else:       
        stock_data_list = []

        with open(filepath, 'rb') as f:
            while True:
                stock_date = f.read(4)
                stock_open = f.read(4)
                stock_high = f.read(4)
                stock_low= f.read(4)
                stock_close = f.read(4)
                stock_amount = f.read(4)
                stock_vol = f.read(4)
                stock_reservation = f.read(4)

                # date,open,high,low,close,amount,vol,reservation
                #print("res:"+ stock_date)

                #print("res" + str(stock_date))
                #print(stock_date)
                if not stock_date:
                    break
                stock_daily_data_dict = {}
                stock_date = struct.unpack("i", stock_date)     # 4字节 如20091229

                # stock_data_str = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d')
                
                stock_open = struct.unpack("i", stock_open)[0]/100     
                stock_high = struct.unpack("i", stock_high)[0]/100.0     
                stock_low= struct.unpack("i", stock_low)[0]/100.0       
                stock_close = struct.unpack("i", stock_close)[0]/100.0   
                stock_amount = struct.unpack("f", stock_amount) #成交额
                stock_vol = struct.unpack("i", stock_vol)       #成交量
                stock_reservation = struct.unpack("i", stock_reservation) #保留值

                stock_daily_data_dict["stock_data_str"] = stock_date[0].__str__()
                stock_daily_data_dict["stock_open"] = stock_open
                stock_daily_data_dict["stock_high"] = stock_high
                stock_daily_data_dict["stock_low"] = stock_low
                stock_daily_data_dict["stock_close"] = stock_close
                stock_daily_data_dict["stock_amount"] = stock_amount
                stock_daily_data_dict["stock_vol"] = stock_vol

                stock_data_list.append(stock_daily_data_dict)

        return stock_data_list    

                # print("stock_open--start--" + str(stock_open) + "--end")
                #print("stock_open--start--" + str(stock_open[0]))# + "--"+ str(stock_open[1])# + "--"+ str(stock_open[2]) + "--")

                # date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
                # list= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_vol[0])+"\r\n"
                # file_object.writelines(list)
        # file_object.close()
        # print("write file end")

# 获取所有的数据
def read_data():
    file_source_dir_path = "/Users/pengcheng.xi/Desktop/量化实践/test/source/"
    listfile = os.listdir(file_source_dir_path)
    stock_code_data_all_dict = {}

    for file in listfile:
        stock_code = file[:-4]
        stock_code_data_all_dict[stock_code] = stock_query(file_source_dir_path + file, stock_code)
    return stock_code_data_all_dict

# 获取指定code、日期的数据
def get_code_date_stock(code, from_date, end_date):
    res = read_data()
    return res[code]

def adapt_echarts(code, from_date, end_date):
    res = get_code_date_stock(code, from_date, end_date)
    stock_data_str_list = []
    stock_open_list = []
    # stock_daily_data_dict["stock_data_str"] = stock_date[0]
    # stock_daily_data_dict["stock_open"] = stock_open
    # stock_daily_data_dict["stock_high"] = stock_high
    # stock_daily_data_dict["stock_low"] = stock_low
    # stock_daily_data_dict["stock_close"] = stock_close
    # stock_daily_data_dict["stock_amount"] = stock_amount
    # stock_daily_data_dict["stock_vol"] = stock_vol
    for stock_daily_data_dict in res:
        stock_data_str_list.append(stock_daily_data_dict["stock_data_str"])
        stock_open_list.append(stock_daily_data_dict["stock_open"])


#定义图片路径

# @route('/resource/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
# def server_static(filename):
#     #"""定义/assets/下的静态(css,js,图片)资源路径"""
#     return static_file(filename, root=assets_path)
# @route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
# def server_static(filename):
#     """定义/assets/字体资源路径"""
#     return static_file(filename, root=assets_path)

assets_path = './assets'

@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)
@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)


@route( "/")
def index():
    stock_code = "sz399608"
    res = get_code_date_stock(stock_code, "", "")
    print(res)
    stock_data_list = []
    stock_open_list = []
    stock_high_list = []
    stock_low_list = []
    stock_close_list = []
    stock_amount_list = []
    stock_vol_list = []
    # stock_daily_data_dict["stock_data_str"] = stock_date[0]
    # stock_daily_data_dict["stock_open"] = stock_open
    # stock_daily_data_dict["stock_high"] = stock_high
    # stock_daily_data_dict["stock_low"] = stock_low
    # stock_daily_data_dict["stock_close"] = stock_close
    # stock_daily_data_dict["stock_amount"] = stock_amount
    # stock_daily_data_dict["stock_vol"] = stock_vol
    for stock_daily_data_dict in res:
        stock_data_list.append(stock_daily_data_dict["stock_data_str"])
        stock_open_list.append(stock_daily_data_dict["stock_open"])
        stock_high_list.append(stock_daily_data_dict["stock_high"])
        stock_low_list.append(stock_daily_data_dict["stock_low"])
        stock_close_list.append(stock_daily_data_dict["stock_close"])
        stock_amount_list.append (stock_daily_data_dict["stock_amount"])
        stock_vol_list.append(stock_daily_data_dict["stock_vol"])

    stock_data_str_list = stock_data_list.__str__()
    stock_open_list = stock_open_list.__str__()
    stock_high_list = stock_high_list.__str__()
    stock_low_list = stock_low_list.__str__()
    stock_close_list = stock_close_list.__str__()
    stock_amount_list = stock_amount_list.__str__()
    stock_vol_list = stock_vol_list.__str__()

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
                text: '折线图堆叠'
            },
            tooltip: {
                trigger:'axis'
            },
            legend: {
                data: ['stock_open', 'stock_high', 'stock_low', 'stock_close']
            },
            grid:{
                left:'13%',
                right:'14%',
                bottom: '13%',
                containLaber:true
            },
            toolbox:{
                feature:{
                    saveAsImage:{}
                }
            },
            xAxis: {
                boundaryGap:false,
                data : '''+stock_data_str_list +'''
            },
            yAxis: {
                type:'value'
            },
            series: [
            {
                name: 'stock_open',
                type: 'line',
                stack:'总量',
                data: '''+stock_open_list+'''
            },
            {
                name: 'stock_high',
                type: 'line',
                stack:'总量',
                data: '''+stock_high_list+'''
            },
            {
                name: 'stock_low',
                type: 'line',
                stack:'总量',
                data: '''+stock_low_list+'''
            },
            {
                name: 'stock_close',
                type: 'line',
                stack:'总量',
                data: '''+stock_close_list+'''
            }
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>
</html> '''    

# if __name__ == '__main__':
#     main()
#     #data = read_data()
#     #print(get_code_date_stock("sz399608", "", ""))



run(host='localhost',port=8080)
