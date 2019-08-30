# -*- coding: utf-8 -*-

'''
parse the tdx file and save to td engineer.
通达信
每32个字节为一天数据
每4个字节为一个字段，每个字段内低字节在前
00 ~ 03 字节：年月日, 整型
04 ~ 07 字节：开盘价*100， 整型
08 ~ 11 字节：最高价*100,  整型
12 ~ 15 字节：最低价*100,  整型
16 ~ 19 字节：收盘价*100,  整型
20 ~ 23 字节：成交额（元），float型
24 ~ 27 字节：成交量（股），整型
28 ~ 31 字节：（保留）
'''


'''
Parse the tdx file.
'''
import struct
import datetime
def parseDatas(filepath, name):
    data = []
    start_time = datetime.datetime.now()
    time_interval = datetime.timedelta(microseconds=1000)
    print(time_interval)
    cnt = 0
    with open(filepath, 'rb') as f:
        cursor, conn = openCursor()
        try:
            while True:      
                stock_date = f.read(4)
                stock_open = f.read(4)
                stock_high = f.read(4)
                stock_low = f.read(4)
                stock_close = f.read(4)
                stock_amount = f.read(4)
                stock_vol = f.read(4)
                stock_reservation = f.read(4)

                if not stock_date:
                    break

                cnt += 1  
                stock_date = struct.unpack("I", stock_date)
                stock_open = struct.unpack("I", stock_open)
                stock_high = struct.unpack("I", stock_high)
                stock_low = struct.unpack("I", stock_low)
                stock_close = struct.unpack("I", stock_close)
                stock_amount = struct.unpack("f", stock_amount)
                stock_vol = struct.unpack("I", stock_vol)
                # f"date-> {stock_date}, open_price -> {stock_open}, high_price->{stock_high}, low_price->{stock_low}, stock_close->{stock_close}, stock amount->{stock_amount},stock_vo->{stock_vol}"
                
                value = f"('{start_time}', '{name}', {stock_date[0]}, {stock_open[0]}, {stock_high[0]}, {stock_low[0]}, {stock_close[0]}, {stock_amount[0]}, {stock_vol[0]})"
                data.append(value)
                start_time += time_interval
                print(start_time)
                if (cnt % 400 == 0):
                    saveToDb(cursor, data)
                    data.clear()
            saveToDb(cursor, data)
            data.clear()
        except Exception as err:
            conn.close()
            data.clear()
            print(err)
    print(f'{cnt} records')

'''
open cursor
'''
def openCursor():
    conn = taos.connect(host='127.0.0.1', database='stocks')
    cursor = conn.cursor()
    return cursor, conn

'''
Save to db
'''
import taos
import pandas as pd
def saveToDb(cursor, values):
    values_str = ' '.join(str(e) for e in values)
    sql = 'insert into stock(stock_timestamp, stock_code, stock_date, stock_open, stock_high, stock_low, stock_close, stock_amount, stock_vol) values ' + values_str
    cursor.execute(sql)

parseDatas('./datas/sh600525.day', 'sh6000525')
