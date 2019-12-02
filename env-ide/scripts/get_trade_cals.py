#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import test.time_hashlib
import h5py  # 导入工具包
import pandas as pd
import datetime
from bs4 import BeautifulSoup

dbfilename = 'TRADE_CAL.h5'
dbkey = 'trade_cal'

def save_trade_days():
    import tushare as ts
    trade_cal = ts.trade_cal()
    trade_cal.to_hdf(dbfilename, key=dbkey, mode='w')

def load_trade_days():
    trade_cal = pd.read_hdf(dbfilename, dbkey)
    trade_days = trade_cal[trade_cal['isOpen'] == 1]
    trade_days = trade_days.loc[:, ['calendarDate']]
    # trade_days['calendarDate'] = pd.to_datetime(trade_days['calendarDate'])
    # today = pd.Timestamp.now()
    # trade_days = trade_days[trade_days['calendarDate'] <= today]
    return trade_days


def testload():
    # save_trade_days()
    trade_days = load_trade_days()
    trade_days = trade_days.iloc[::-1]  # reverse
    # trade_days.to_csv("test.csv", index=False, header=False)
    print(trade_days.head())
    return trade_days

def parse_url(selectedDate='2019-11-01'):
    import requests

    cookies = {
        'route': '5381fa73df88cce076c9e01d13c9b378',
        'ASP.NET_SessionId': 'owusxurvetxp0kn20zab2ez4',
        'UM_distinctid': '16e346230a814c-0771297b1f1cf7-1d3c6a5a-13c680-16e346230a924c',
        'guid': '8b5cfc25-26d9-44e4-08de-e9d1cf0fc590',
        'Hm_lvt_44c27e8e603ca3b625b6b1e9c35d712d': '1572836882',
        'CNZZDATA1269807659': '1819591522-1572835372-%7C1573106138',
        'STATReferrerIndexId': '1',
        'isCloseOrderZHLayer': '0',
        'Hm_lpvt_44c27e8e603ca3b625b6b1e9c35d712d': '1573106578',
    }

    headers = {
        'Connection': 'keep-alive',
        'Origin': 'http://www.sci99.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
        'DNT': '1',
        'Accept': '*/*',
        'Referer': 'http://www.sci99.com/targetprice/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    data = {
        'ScriptManager1': 'UpdatePanel1|btn_search',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUKLTkyMzE2ODU4NGRkuNeScNjYAmnyJCCB1Mq+4j4AEJs=',
        '__VIEWSTATEGENERATOR': 'F19A430D',
        '__EVENTVALIDATION': '/wEdAAObbRVIA/CBBHfOMLCwpcNEjh1eB+RmMBQ9g5SArgqYH1/dZjW/tHAJcLmf/EpfSVz42hutvzz550coI8C39XJyOjE0fg==',
        'selecttime': selectedDate,
        '__ASYNCPOST': 'true',
        'btn_search': ''
    }
    response = requests.post('http://www.sci99.com/targetprice/',
                            headers=headers, cookies=cookies, data=data, verify=False)
    if(response.status_code == 200):
        pass
    else:
        print("Get %s error status" % selectedDate, response.status_code)
    return response.text

def get_price_df(div, datestr):
    price_list = div.find_all(class_='price_list')
    # colnames = ['date', 'LLDPE', 'carbinol', 'LNG', 'rebar3',
    #             'fdcejd_brown', 'sylq_a_70', 'SCRWF', 'PP_YARN', 'corn_starch', 'pig', 'carbamide', 'strip_steel']
    df = None
    print(len(price_list))
    if(len(price_list) > 0):
        dataSet = {}
        # dataSet.insert(0, datestr)
        dataSet['date'] = datestr
        for ul_price_ele in price_list:
            lis = ul_price_ele.find_all('li')
            if(len(lis) == 5):
                name = lis[0].text
                price = lis[2].text
                # dataSet.append({name:price})
                dataSet[name] = price
                pass
        print('-=-=-=-=-=-=-=-=-=-', datestr)
        
        # arr = np.array(dataSet)
        # dfarr = pd.DataFrame(arr)
        # print(arr)
        # print(len(arr), len(colnames))
        # print(dfarr)
        # print(dfarr.T)
        print(dataSet)
        # df = pd.DataFrame(dataSet, columns=colnames)
        # df = pd.DataFrame([dataSet])
        df = pd.DataFrame(dataSet, index=[0])
        return df
    else:
        print("holiday or no data")
    return None

def parse_html(datestr, sleeptime=2):
    import time
    import os
    resptxt = parse_url(selectedDate=datestr)
    soup = BeautifulSoup(resptxt, 'lxml')
    div = soup.find('div', class_='list_cont')
    df = get_price_df(div, datestr)
    if(df is not None):
        filename = "main_csv.h5"
        dfdest = df
        print(dfdest)
        if(os.path.exists(filename) and os.stat(filename).st_size > 0):
            srcdf = pd.read_csv(filename)
            if(len(srcdf)>0):
                dfdest = pd.concat([srcdf, df], sort=False)
        # print(dfdest)
        dfdest.to_csv(filename, mode='w', header=True, index=False)
    # print(datestr)
    time.sleep(sleeptime)
    # price_list = div.find_all(class_='price_list')
    # dataSet = []
    # colnames = ['date', 'name', 'unit', 'price', 'diff_price', 'diff_rate']
    # df = pd.DataFrame()
    # if(len(price_list) > 0) :
    #     for index,ul_price_ele in price_list:
    #         lis = ul_price_ele.find_all('li')
    #         if(len(lis) == 5):
    #             row = []
    #             for li in lis:
    #                 row.append(li.text)
    #             row.insert(0, datestr)
    #             # print(row)
    #             dataSet.append(row)
    #             # print(dataSet)
    #             # rowdf = pd.DataFrame(row, columns=colnames)
    #             # 
    #         print('-=-=-=-=-=-=-=-=-=-', datestr)
    #     df = pd.DataFrame(dataSet, columns=colnames)
    #     print(df)
    # else:
    #     print("holiday or no data")
    return df

def handle_onelist(one_list, n):
    if(one_list is None) : return
    for index, row in one_list.iterrows():
        day = one_list.loc[index, 'calendarDate']
        print(day)

import math
def load_dates():
    trade_days = load_trade_days()
    trade_days = trade_days.iloc[::-1]  # reverse
    rstdf = []
    colname = 'calendarDate'
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    start_date = '2008-01-01'
    trade_days[colname] = pd.to_datetime(
        trade_days[colname], dayfirst=True)
    mask = (trade_days[colname] > start_date) & (trade_days[colname] <= today)
    trade_days1 = trade_days.loc[mask]
    length = len(trade_days1)
    print(length)
    # print(trade_days1.head(2))
    # print(trade_days1.tail(2))

    n = 4
    for i in range(n):
        one_list = trade_days1[math.floor(i / n * length):math.floor((i + 1) / n * length)]
        print(i)
        if(i==3):
            handle_onelist(one_list, i)
        print(len(one_list))
        print(one_list.head(2))
        print(one_list.tail(2))
    
    # today = '2016-10-19'
    # print(today)

    # maindf = pd.DataFrame()
    # for index,row in trade_days.iterrows():
    #     day = trade_days.loc[index, 'calendarDate']
    #     if(day>today):
    #         continue
    #     df = parse_html(day)
    #     # df.to_hdf("data/%s.h5" % day, key="data", mode='w',
    #     #             complib="blosc:snappy", complevel=5)
    #     maindf = maindf.append(df, ignore_index=True)
    #     # print(maindf.tail(2))
    # #     rstdf.append(df)
    # maindf.to_csv("main.csv")
    print("done")
    # maindf.to_hdf("main.h5", key="data", mode='w', complib="blosc:snappy", complevel=5)
    # maindf = pd.concat(rstdf)

import os
def mergeh5():
    folder = "data"
    files = os.listdir(folder)
    rstdf = []
    maindf = pd.DataFrame()
    for fname in files:  # 遍历文件夹
        if not os.path.isdir(fname):  # 判断是否是文件夹，不是文件夹才打开
            fullname = "{0}/{1}".format(folder, fname)
            print(fullname)
            dfr = pd.read_hdf(fullname, 'data')
            maindf = maindf.append(dfr, ignore_index=True)
    maindf.to_csv("main.csv", index=False)
    maindf.to_excel("main.xls", index=False)
    print(len(maindf))
    # dfr.to_hdf("2019-11-06.h5", 'data')
    # print(dfr)

def test():
     dfr = pd.read_hdf("data/2016-10-19.h5", 'data')
     print(dfr)

def main():
    # test()
    # mergeh5()
    load_dates()
    # parse_html('2019-11-01')
    # parse_html('2019-10-31')
    # parse_html('2010-01-04')
    # parse_html('2010-01-05')
    # print('2019-01-03'>'2019-02-02')
    print("-end-")

if __name__ == '__main__':
    main()
    # print(get_proxy_ips())
