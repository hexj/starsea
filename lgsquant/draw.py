from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
import os
import struct
import pandas as pd
import sys


# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar,Kline,Line

df = []
data =[]

def CalMA(df, n):
     df = df.join(pd.Series(df['close'].rolling(n).mean(), name = 'MA' + str(n)))
     return df['MA' + str(n)]


def exitProgram(conn):
    conn.close()
    sys.exit()

def parse_tdxfile(fname):
    dataSet=[]
    with open(fname,'rb')  as fl:
        buffer=fl.read()  #读取数据到缓存
        size=len(buffer)
        rowSize=32 #通信达day数据，每32个字节一组数据
        code=os.path.basename(fname).replace('.day','')
        for i in range(0,size,rowSize):  #步长为32遍历buffer
            row=list( struct.unpack('IIIIIfII',buffer[i:i+rowSize]) )
            row[1]=row[1]/100
            row[2]=row[2]/100
            row[3]=row[3]/100
            row[4]=row[4]/100
            row.pop() #移除最后无意义字段
            row.insert(0,code)
            dataSet.append(row)
    df = pd.DataFrame(data=dataSet,columns=['code','tradeDate','open','high','low','close','amount','vol'])
    return df

def parse_folder(folder_name):
    print(folder_name)
    path = folder_name
    files= os.listdir(path)
    for fname in files: #遍历文件夹
        if not os.path.isdir(fname): #判断是否是文件夹，不是文件夹才打开
            fullname = "{0}/{1}".format(folder_name, fname)
            print(fullname)
            df = parse_tdxfile(fullname)
            # TODO save to ?

app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


def kline_datazoom_inside() -> Kline:
    c = (
        Kline()
        .add_xaxis(["2017/7/{}".format(i + 1) for i in range(31)])
        .add_yaxis("kline", data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title="Kline-DataZoom-inside"),
        )
    )
    return c

def kline_itemstyle() -> Kline:
    a=["2017/7/{}".format(i + 1) for i in range(31)]
    b=df['tradeDate'].values.tolist()
    c=data
    d=df[['open','close','high','low']].values.tolist()
    print(c)
    print(d)
    c = (
        Kline()
        .add_xaxis(b)
        .add_yaxis(
            "日K",
            d,
            itemstyle_opts=opts.ItemStyleOpts(
                color="#ec0000",
                color0="#00da3c",
                border_color="#8A0000",
                border_color0="#008F28",
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title="sh000001.day"),
        )
    )
    c.overlap(Ma(5))
    c.overlap(Ma(10))
    c.overlap(Ma(15))
    return c

def Ma(n) -> Line:
    a=df['tradeDate'].tolist()
    print(a)
    b=["2017/7/{}".format(i + 1) for i in range(7012)]
    print(b)
    c=CalMA(df,n).values.tolist()
    print(c)
    d=[2400.1231212312121242342+i for i in range(7012)]
    print(d)
    c = (
       Line()
        .add_xaxis(a)
        .add_yaxis("Ma"+str(n),c,is_smooth=True,is_symbol_show=False)
        .set_series_opts(
           label_opts=opts.LabelOpts(is_show=False),
       )
    )

    return c


@app.route("/")
def index():
    c = kline_itemstyle()
    #c = Ma(5)
    return Markup(c.render_embed())


if __name__ == "__main__":
    folder_name = "/Users/lgs/Documents/sh-sz-lday-2004-20190821"
    fname = folder_name + "/sh000001.day"
    # parse_folder(folder_name)
    df = parse_tdxfile(fname)
    df['tradeDate']=pd.to_datetime(df['tradeDate'],format="%Y%m%d")
    df['tradeDate']=df['tradeDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
    print(df)
    app.run()