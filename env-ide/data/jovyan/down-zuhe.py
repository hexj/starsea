# -*- coding: utf-8 -*-
import urllib.request
import json
headers = {#'X-Requested-With': 'XMLHttpRequest',
           #'Referer': 'http://xueqiu.com/p/ZH010389',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
           #'Host': 'xueqiu.com',
           #'Connection':'keep-alive',
           #'Accept':'*/*',
           'cookie':'s=iabht2os.1dgjn9z; xq_a_token=02a16c8dd2d87980d1b3ddced673bd6a74288bde; xq_r_token=024b1e233fea42dd2e0a74832bde2c914ed30e79; __utma=1.2130135756.1433017807.1433017807.1433017807.1;'
           '__utmc=1; __utmz=1.1433017807.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1433017809; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1433017809'}
url = 'http://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389&count=20&page=1'
req = urllib.request.Request(url,headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8')
#print(html)
data = json.loads(html)
print('股票名称',end=':')
print(data['list'][0]['rebalancing_histories'][0]['stock_name'],end='   持仓变化')
print(data['list'][0]['rebalancing_histories'][0]['prev_weight'],end='-->')
print(data['list'][0]['rebalancing_histories'][0]['target_weight'])
print('股票名称',end=':')
print(data['list'][0]['rebalancing_histories'][1]['stock_name'],end='   持仓变化')
print(data['list'][0]['rebalancing_histories'][1]['prev_weight'],end='-->')
print(data['list'][0]['rebalancing_histories'][1]['target_weight'])
