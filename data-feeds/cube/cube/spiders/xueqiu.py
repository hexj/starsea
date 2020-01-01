# -*- coding: utf-8 -*-
import scrapy
import json
from cube.crack.xueqiu_login import CrackXueQiu
from cube.spiders.hdf5 import Hdf5Utils
from scrapy.loader import ItemLoader
from cube.items import CubeItem, OwnerItem
from scrapy.loader.processors import Join, MapCompose, SelectJmes
from bs4 import BeautifulSoup
import redis


class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']
    login_result = True
    cookiestr = ''
    send_headers = {}
    cube_discover_url = 'https://xueqiu.com/cubes/discover/rank/cube/list.json?category=14&count=20&page='
    cube_info_url = 'https://xueqiu.com/P/'
    # 调仓历史
    cube_rebalce_url = 'https://xueqiu.com/cubes/rebalancing/history.json?count=20&page=1&cube_symbol='
    # 收益历史
    cube_profilt_url = 'https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol='
    r = redis.Redis(host='localhost', password='123456')
    # 是否用指定的代码爬取数据
    readSpecifySymbol = False
    # 指定的组合代码
    symbols = ['ZH009248']
    hdf5 = Hdf5Utils()
    # dictionary to map UserItem fields to Jmes query paths
    jmes_paths = {
        'name': 'name',
        'symbol': 'symbol',
        'market': 'market',
        'net_value': 'net_value',
        'daily_gain': 'daily_gain',
        'monthly_gain': 'monthly_gain',
        'total_gain': 'total_gain',
        'annualized_gain': 'annualized_gain',
        'closed_at': 'closed_at',  # 这个字段如果为空，则表示未关闭状态
        'owner': 'owner'
    }

    owner_jmes_paths = {
        'id': 'id',
        'screen_name': 'screen_name'
    }

    def __init__(self):
        crack = CrackXueQiu()
        self.login_result = crack.crack()
        pass

    def start_requests(self):
        if not self.login_result:
            print('自动登录不成功，停止')
            pass

        with open('tmp_data/xueqiu_cookie.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        cookie = [item["name"] + "=" + item["value"] for item in listCookies]
        self.cookiestr = '; '.join(item for item in cookie)
        print(f'从文件中读取的cookie: {self.cookiestr}')
        self.send_headers = {
            'cookie': self.cookiestr,
            # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        '''
        profit_list:
        所有的收益：https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol=ZH1067693
        rebalance_list:
        调仓历史：https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH009248&count=20&page=1

        '''
        self.readSpecifySymbol = True
        self.symbols = ['ZH009248']
        if self.readSpecifySymbol:
            for s in self.symbols:
                yield scrapy.Request(f'{self.cube_profilt_url}{s}', self.parseCubeProfitList, headers=self.send_headers)
                yield scrapy.Request(f'{self.cube_rebalce_url}{s}', self.parseCubeRebalanceList,
                                     headers=self.send_headers, cb_kwargs=dict(symbol=s))
            pass
        else:
            # print(f'headers的内容是：{send_headers}')
            # print({cookiestr})
            currentPage = 1
            finalUrl = f'{self.cube_discover_url}{currentPage}'
            yield scrapy.Request(finalUrl, headers=self.send_headers)

    def parseCubeProfitList(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        print('type of the result is1:' + str(len(jsonresponse)))
        symbol = jsonresponse[0]['symbol']

        h5name = f"cube_info_{symbol}.h5"
        self.hdf5.save_data_via_pandas(h5Name=h5name, key="profit_list", dataList=jsonresponse[0]['list'])

    def parseCubeRebalanceList(self, response, symbol):
        jsonresponse = json.loads(response.body_as_unicode())
        print('type of the result is2:' + str(len(jsonresponse)))
        page = jsonresponse['page']
        maxPage = jsonresponse['maxPage']

        print(f'------------进行第{page}数据爬取')

        if page < maxPage:
            page += 1
            self.cube_rebalce_url = f"https://xueqiu.com/cubes/rebalancing/history.json?count=20&page={page}&cube_symbol={symbol}"
            print(self.cube_rebalce_url)
            yield scrapy.Request(self.cube_rebalce_url, self.parseCubeRebalanceList, headers=self.send_headers,
                                 cb_kwargs=dict(symbol=symbol))

        h5name = f"cube_info_{symbol}.h5"

        dataList = []
        self.hdf5.save_data_via_pandas(h5Name=h5name, key="rebalance_list", dataList=jsonresponse['list'],
                                       exclude=['rebalancing_histories'])
        for history in jsonresponse['list']:
            dataList += history['rebalancing_histories']
        if len(dataList) > 0:
            self.hdf5.save_data_via_pandas(h5Name=h5name, key="rebalancing_histories", dataList=dataList, fillna=True)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        # yield jsonresponse

        for c in jsonresponse['list']:
            loader = ItemLoader(item=CubeItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')

            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(c))
            item = loader.load_item()

            ownerLoader = ItemLoader(item=OwnerItem())
            ownerLoader.default_input_processor = MapCompose(str)
            ownerLoader.default_output_processor = Join(' ')
            for (field, path) in self.owner_jmes_paths.items():
                ownerLoader.add_value(field, SelectJmes(path)(c['owner']))
            owner = ownerLoader.load_item()

            item['owner'] = owner
            yield item

            # 开始提取用户信息
            uid = owner['id']
            # https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid=6626771620&pid=-24（创建的组合）
            createdCubeUrl = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-24'
            #  请求用户创建的组合
            # 通过cb_kwargs的方式，给解析函数传递参数
            yield scrapy.Request(createdCubeUrl, self.parseCubeList, headers=self.send_headers,
                                 cb_kwargs=dict(uid=uid, screen_name=owner['screen_name']))

            # 请求用户关注的组合，这个地方不去传递uid和screen_name信息，这种情况下，通过请求网页去解析，
            # TODO 请求网页的速度超慢，想办法优化，开启多线程？
            followedCubeUrl = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-120'
            yield scrapy.Request(followedCubeUrl, self.parseCubeList, headers=self.send_headers)

            # 组合信息：
            # https://xueqiu.com/cubes/quote.json?code=ZH976766,SP1034535,SP1012810,ZH1160206,ZH2003755,ZH1996976,ZH1079481,ZH1174824,ZH1079472,SP1040320

        page = jsonresponse['page']
        maxPage = jsonresponse['maxPage']
        if (page < maxPage):
            url = f'{self.cube_discover_url}{page + 1}'
            yield scrapy.Request(url, headers=self.send_headers)

    def parseCubeList(self, response, uid=None, screen_name=None):
        '''
        通过去查找创建的组合以及组合的基本信息
        '''
        jsonresponse = json.loads(response.body_as_unicode())

        stockJson = jsonresponse['data']['stocks']

        symbolListStr = (",".join(str(s['symbol']) for s in stockJson))
        symbolList = symbolListStr.split(',')

        if uid is None:
            for s in symbolList:
                yield scrapy.Request(f'{self.cube_info_url}{s}', self.parseCubeDetailInfo, cb_kwargs=dict(symbol=s),
                                     headers=self.send_headers)
        else:
            cubeInfoUrl = 'https://xueqiu.com/cubes/quote.json?code=' + symbolListStr
            yield scrapy.Request(cubeInfoUrl, self.parseCubeInfo, headers=self.send_headers,
                                 cb_kwargs=dict(uid=uid, screen_name=screen_name, symbolList=symbolList))

    def parseCubeDetailInfo(self, response, symbol):
        '''
        解析组合的详细详细信息
        '''
        soup = BeautifulSoup(response.text, 'html.parser')
        uid = soup.find("a", {"class": "creator"})['href'][1:]
        screen_name = soup.find("div", {"class": "name"}).text
        symbolList = [symbol]
        cubeInfoUrl = 'https://xueqiu.com/cubes/quote.json?code=' + symbol
        yield scrapy.Request(cubeInfoUrl, self.parseCubeInfo, headers=self.send_headers,
                             cb_kwargs=dict(uid=uid, screen_name=screen_name, symbolList=symbolList))

    def parseCubeInfo(self, response, uid, screen_name, symbolList):
        jsonresponse = json.loads(response.body_as_unicode())
        for s in symbolList:
            loader = ItemLoader(item=CubesItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')
            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(jsonresponse[s]))
            item = loader.load_item()
            owner = OwnerItem()
            owner['id'] = uid
            owner['screen_name'] = screen_name
            item['owner'] = owner
            yield item
