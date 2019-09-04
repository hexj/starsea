#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import struct
import pandas as pd

import sys
import datetime
import random
import time

def exitProgram(conn):
    conn.close()
    sys.exit()
def getconn():
    conn = taos.connect(host="127.0.0.1", user="root", password="taosdata", config="/etc/taos")
    return conn
def df2db(df):
    df.to_sql(name='test', con=con, if_exists='append', index=False)

folder_name = "/Users/hexj/tools/data/sh-sz-lday-2004-20190821"
h5file = "dayochlv.h5"

def parse_tdxfile(fname):
    dataSet=[]
    colnames = ['code','tradeDate','open','high','low','close','amount','vol']
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
            print(len(row))
            print("======")
            row.pop() #移除最后无意义字段
            row.insert(0,code)
            dataSet.append(row)  
    df = pd.DataFrame(data=dataSet, columns=colnames)
    return df

def parse_folder(folder_name):
    print(folder_name)
    path = folder_name
    files= os.listdir(path)
    rstdf = []
    for fname in files: #遍历文件夹
        if not os.path.isdir(fname): #判断是否是文件夹，不是文件夹才打开
            fullname = "{0}/{1}".format(folder_name, fname)
            print(fullname)
            df = parse_tdxfile(fullname)
            rstdf.append(df)
    maindf = pd.concat(rstdf)
    return maindf

from sqlalchemy import * 
def writetable(df):
    engine=create_engine("mysql+pymysql://root:a5230411@localhost:3306/test",echo=True)
    metadata=MetaData(engine)

def concattest():
    fname = folder_name +"/sh000001.day"
    fname2 = folder_name +"/sh000002.day"
    df1 = parse_tdxfile(fname)
    # df2 = parse_tdxfile(fname2)
    # maindf = pd.concat([df1,df2])
    # maindf[['tradeDate']>=20190821 & ['tradeDate']<=20190823]
    # print(maindf['tradeDate'].tail())
    # print(maindf.tail())
    # print(len(maindf))
    import taos
    df1

def writeall():
    # folder_name = "/Users/hexj/tools/data/tmp"
    maindf = parse_folder(folder_name)
    maindf.to_hdf(h5file, key="dayochlv", mode='a', complib="blosc:snappy", complevel=5)
    print(len(maindf))
    print(maindf.tail())
    dfr = pd.read_hdf(h5file, 'dayochlv')
    print(len(dfr))

def main(): 
    concattest()
    # writeall()

    # colnames = ['code','tradeDate','open','high','low','close','amount','vol']
    # print(colnames.index('tradeDate'))
    print("-end-")


def _time_analyze_(func):
    t1_start = time.perf_counter()  
    func()
    t1_stop = time.perf_counter() 
    print(func.__name__)
    print("Elapsed time: %s s" % (t1_stop - t1_start))

if __name__ == '__main__':
    _time_analyze_(main)
    