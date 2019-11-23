#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import  BeautifulSoup
import requests
import re
import time
import json
import mysql.connector



class TTJJ_Fund(object):

    def __init__(self):
        self.xh=''; #序号
        self.jjdm='' #基金代码
        self.jjname='' #基金简称
        self.dwjz='' #单位净值
        self.ljjz='' #累计净值
        self.rzzz='' #日增长值
        self.rzzl='' #日增长率
        self.sgzt='' #申购状态
        self.shzt='' #赎回状态
        self.sxf=''#手续费
        self.jjb_url=''#基金吧的地址
        self.jjda_url=''#基金档案的地址



    def __str__(self):
        return '序号:'+self.xh+',基金代码:'+self.jjdm+',金简称:'+self.jjname+',单位净值:'+self.dwjz+',累计净值:'+self.ljjz+':日增长值'+self.rzzz+',日增长率:'+self.rzzl+',赎回状态:'+ self.shzt+', 申购状态:'+  self.sgzt+',手续费:'+ self.sxf

class TTJJ_LJJZ_Fund(object):
    def __init__(self):
        self.date='' #日期
        self.dwjz='' #单位净值
        self.lljz='' #累计净值
        # self.sdate='' #不清楚
        # self.actualsyi='' #实际价值
        self.sgzt='' #申购状态
        self.shzt='' #赎回状态

    def __str__(self):
        return '日期:'+self.date+',单位净值:'+self.dwjz+',累计净值:'+self.lljz+',申购状态:'+self.sgzt+',赎回状态:'+self.shzt



if __name__ =='__main__':
    url='http://fund.eastmoney.com/jzzzl.html'
    req=requests.get(url)
    req.encoding='gb2312'
    html=req.text
    bf = BeautifulSoup(html, 'lxml')
    div = bf.find_all('div', id='tableDiv')
    div_bf = BeautifulSoup(str(div[0]), 'lxml')
    tbody= div_bf.find_all('tbody')
    tbody_bf = BeautifulSoup(str(tbody[0]), 'lxml')
    trs = tbody_bf.find_all('tr')
    count=len(trs[:])
    print(str(count))

    fund_list=[]
    for index in range(count):

        fund = TTJJ_Fund()

        tr_bf = BeautifulSoup(str(trs[index]), 'lxml')

        xh = tr_bf.find_all('td',class_ = 'xh')
        fund.xh=xh[0].string

        bzdm = tr_bf.find_all('td',class_ = 'bzdm')
        fund.jjdm=bzdm[0].string

        nobr=tr_bf.find_all('nobr')
        nobr_bf = BeautifulSoup(str(nobr[0]), 'lxml')
        nobr_a = nobr_bf.find_all('a')

        fund.jjname=nobr_a[0].get('title')
        fund.jjb_url=nobr_a[2].get('href')

        dwjz = tr_bf.find_all('td',class_ = 'dwjz black')
        fund.dwjz=dwjz[0].string


        ljjz = tr_bf.find_all('td',class_ = 'ljjz black')
        fund.ljjz=ljjz[0].string


        rzzz_red = tr_bf.find_all('td',class_ = 'rzzz red')
        fund.rzzz=rzzz_red[0].string

        rzzl_bg_red = tr_bf.find_all('td',class_ = 'rzzl bg red')
        fund.rzzl=rzzl_bg_red[0].string

        sgzt = tr_bf.find_all('td',class_ = 'sgzt')
        fund.sgzt=sgzt[0].string

        shzt = tr_bf.find_all('td',class_ = 'shzt')
        fund.shzt=shzt[0].string

        a_zkf=tr_bf.find_all('a',class_ ='zkf')

        if(a_zkf.__len__()>0):
            fund.sxf = a_zkf[0].string
            fund.jjda_url=a_zkf[0].get('href')

        #print(fund.__str__())
        fund_list.append(fund)
    div_pager = bf.find_all('div', class_='div-pager')
    span = div_pager[0].find_all('span',class_='nv')
    #print(str(span))

    number=re.findall(r'\d+', str(span[0]))
    #print(str(number[0]))

    fund_page_url='http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc'

    for index in range(2,int(number[0])):
        pager = '&page=' + str(index)+',200'
        t = time.time()
        dt='&dt='+str(int(round(t * 1000)))
        end='&atfc=&onlySale=0'
        requests_url=fund_page_url+pager+dt+end
        req = requests.get(requests_url)
        pager_result = req.text

        datas_pager_result_split=pager_result.split('datas:')
        count_pager_result_split=datas_pager_result_split[1].split(',count:')
        json_array = json.loads(count_pager_result_split[0],encoding='utf-8')
        for jba in json_array:
            fund_ = TTJJ_Fund()
            fund.xh = jba[14]
            fund.jjdm = jba[0]
            fund.jjname = jba[1]
                #fund.jjb_url =''
            fund.dwjz = jba[3]
            fund.ljjz = jba[4]
            fund.rzzz = jba[7]
            fund.rzzl = jba[8]+'%'
            fund.sgzt = jba[9]
            fund.shzt = jba[10]
            fund.sxf  = jba[17]
            fund_list.append(fund)

            # for fd in fund_list:
            #     print(fd.__str__())

    # 打印每个基金的历史净值
    t = time.time()
    time_now = str(int(round(t * 1000)))  # 当前的时间

    time_pre = str(int(round(t * 1000)) - 30 * 1000)  # 进入网页的时间戳



    # code = '001838'

    pageSize = 20

    time.sleep(1)

    mydb = mysql.connector.connect(
        host="127.0.0.1",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="12345678",  # 数据库密码
        auth_plugin='mysql_native_password',
        database='fund_database'
    )


    for fd in fund_list:
        code = fd.jjdm

        mycursor = mydb.cursor()
        create_sql = "CREATE TABLE IF NOT EXISTS FUND_LSJZ_" + code + " ( id INT AUTO_INCREMENT PRIMARY KEY,fd_date VARCHAR(255),lljz VARCHAR(255),dwjz  VARCHAR(255),sgzt VARCHAR(255) ,shzt VARCHAR(255))"
        print(create_sql)
        mycursor.execute(create_sql)
        total_size = 0

        for index in range(1, 100):
            url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18303333554012487365_' + time_pre + '&fundCode=' + code + '&pageIndex=' + str(
                index) + '&pageSize=' + str(pageSize) + '&startDate=&endDate=&_=' + time_now
            headers = {
                'Referer': 'http://fundf10.eastmoney.com/jjjz_' + code + '.html'
            }
            res = requests.get(url, headers=headers)
            response = res.text
            result_split = response.split(time_pre + '(')
            response_json = result_split[1][:-1]
            json_res = json.loads(response_json, encoding='utf-8')

            fund_lsjz_list = []

            if 0 == json_res.get('ErrCode'):
                json_data = json_res.get('Data')
                list = json_data.get('LSJZList')
                total_size = json_res.get('TotalCount')

                size = len(list)

                for index in range(size):
                    json_fund = list[index]
                    fund = TTJJ_LJJZ_Fund()
                    fund.date = json_fund.get('FSRQ')
                    if fund.date is None:
                        fund.date = ''
                    fund.lljz = json_fund.get('LJJZ')
                    if fund.lljz is None:
                        fund.lljz = ''
                    fund.dwjz = json_fund.get('DWJZ')
                    if fund.dwjz is None:
                        fund.dwjz = ''
                    # fund.sdate=json_fund.get('SDATE','')
                    # fund.actualsyi=json_fund.get('ACTUALSYI','')
                    fund.sgzt = json_fund.get('SGZT')
                    if fund.sgzt is None:
                        fund.sgzt = ''
                    fund.shzt = json_fund.get('SHZT')
                    if fund.shzt is None:
                        fund.shzt = ''

                    fund_lsjz_list.append(fund)

                    sql = "INSERT INTO FUND_LSJZ_" + code + " (fd_date, lljz,dwjz,sgzt,shzt) VALUES (%s, %s,%s,%s,%s)"
                    val = (fund.date, fund.lljz, fund.dwjz, fund.sgzt, fund.shzt);
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("1 条记录插入, ID:"+str(mycursor.lastrowid)+','+fund.__str__())

                if total_size - index * pageSize <= 0:
                    break;
            time.sleep(1)
        print('基金序号：'+str(fd.xh)+'基金名称：'+fd.jjname+',基金代码：'+str(code)+''+'的基金 历史数据合计：'+str(total_size))



