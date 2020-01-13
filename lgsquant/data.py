import pandas
from jqdatasdk import *
import pymysql
import requests
import json
from datetime import  date,timedelta
import signal
import datetime
import time

def tots(str):
    timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray))
def last_time():
    begin_unix = tots(date.today().strftime("%Y-%m-%d 09:00:00"))
    end_unix = tots(date.today().strftime("%Y-%m-%d 15:00:00"))
    now_unix = tots(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if now_unix < end_unix:
        return (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d 23:59:59")
    else:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def today_zero():
    return date.today().strftime("%Y-%m-%d 00:00:00")

def exec_sql(sql):
    print(sql)
    r = requests.post('http://X:X/rest/sql', data=sql,
                      headers={'Authorization': 'Basic cm9vdDp0YW9zZGF0YQ=='})
    print(r.text)
    return r.text

def gain_metadata():
    auth('XXX', 'XXX')
    db = pymysql.connect()
    cursor = db.cursor()
    ###采集股票基本信息
    for row_index,row in pandas.DataFrame(get_all_securities(types=['stock','index','fund'], date=None)).iterrows():
        cursor.execute("insert into quant.stock_index_fund(code,display_name,name,start_date,end_date,type) values('%s','%s','%s','%s','%s','%s') on duplicate key update code='%s',display_name='%s',name='%s',start_date='%s',end_date='%s',type='%s'" % (row_index,row['display_name'],row['name'],row['start_date'],row['end_date'],row['type'],row_index,row['display_name'],row['name'],row['start_date'],row['end_date'],row['type']))
        db.commit()
def gain_data():
    auth('XXX','XXX')
    db = pymysql.connect(host='127.0.0.1')
    cursor = db.cursor()
    cursor.execute("update quant.stock_index_fund set update_ts=now() where end_date < now() and type not in ('stock','index')")
    db.commit()
    cursor.execute("select code,start_date,end_date,type from quant.stock_index_fund where update_ts < '%s' and type not in ('stock','index')" % today_zero())
    rs=cursor.fetchall()
    for row in rs:
        real_code=row[0]
        code=row[0].split('.')
        tbname=code[1]+code[0]+"_"+row[3]+"_daily"
        start_date=row[1].strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('create table IF NOT EXISTS  quant.%s (ts timestamp unique key not null,open float,close float,high float,low float,volume bigint,money bigint)' % tbname)
        cursor.execute('select max(ts) from quant.%s' % tbname)
        curdate_rs=cursor.fetchone()
        if curdate_rs[0]!=None:
            start_date=curdate_rs[0].strftime('%Y-%m-%d %H:%M:%S')
        values=[]
        print(start_date)
        print(last_time())
        if start_date.split(' ')[0] == last_time().split(' ')[0]:
            cursor.execute("update quant.stock_index_fund set update_ts=now() where code='%s'" % real_code)
            db.commit()
            continue
        print(get_query_count())
        for row_index,row in pandas.DataFrame(get_price(row[0], start_date=start_date,end_date=last_time(), frequency='daily', fields=None, skip_paused=True, fq='pre',
                    count=None)).iterrows():
            values.append("('%s',%f,%f,%f,%f,%d,%d)" % (row_index,row['open'],row['close'],row['high'],row['low'],row['volume'],row['money']) )
            if len(values)==500:
                 print("insert ignore into quant.%s(ts,open,close,high,low,volume,money) values%s" % (tbname,",".join(values)))
                 cursor.execute("insert ignore into quant.%s(ts,open,close,high,low,volume,money) values%s" % (tbname,",".join(values)))
                 db.commit()
                 print(values)
                 values=[]
        if len(values)!=0:
            cursor.execute("insert ignore into quant.%s(ts,open,close,high,low,volume,money) values%s" % (tbname,",".join(values)))
            db.commit()
if __name__ == '__main__':
    gain_metadata()
    def handler(signum, frame):
        raise AssertionError
    while True:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(10)
            gain_data()
            signal.alarm(0)
        except AssertionError:
            print("超时重试...")


