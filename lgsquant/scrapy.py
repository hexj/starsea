import requests
from bs4 import BeautifulSoup
from selenium import webdriver
headers1 = {
'Host': 'movie.douban.com',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7'
}

link='https://movie.douban.com/top250?start=25'

r=requests.get(link,headers=headers1)
rs=BeautifulSoup(r.text,"lxml")
div_list=rs.find_all('div',class_='star')

driver = webdriver.Chrome(executable_path='/Users/lgs/Downloads/软件包/chromedriver')
driver.get("https://www.baidu.com")


