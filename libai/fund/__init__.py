#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import  BeautifulSoup
import requests
import re
import time
import json



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
            fund = TTJJ_Fund()
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
    for fd in fund_list:
        print(fd.__str__())