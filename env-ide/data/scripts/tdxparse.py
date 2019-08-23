#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import struct
import pandas as pd

import taos
import sys
import datetime
import random

def exitProgram(conn):
    conn.close()
    sys.exit()
def getconn():
    conn = taos.connect(host="127.0.0.1", user="root", password="taosdata", config="/etc/taos")
    return conn
def df2db(df):
    df.to_sql(name='test', con=con, if_exists='append', index=False)

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

def main(): 
    folder_name = "/Users/hexj/tools/data/sh-sz-lday-2004-20190821"
    fname = folder_name +"/sh000001.day"
    # parse_folder(folder_name)
    df = parse_tdxfile(fname)
    print(df.tail())
    print("-end-")

if __name__ == '__main__':
    main()