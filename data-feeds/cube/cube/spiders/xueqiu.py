# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, SelectJmes
from bs4 import BeautifulSoup
import redis
import os
import time

from cube.config.cube_settings import *
from cube.items import CubeItem, OwnerItem
from cube.crack.xueqiu_login import CrackXueQiu
from cube.spiders.hdf5 import Hdf5Utils


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
    cube_rebalance_url = 'https://xueqiu.com/cubes/rebalancing/history.json?count=20&page=1&cube_symbol='
    # 收益历史
    cube_profilt_url = 'https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol='
    r = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWD)
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
        pass
        # crack = CrackXueQiu()
        # self.login_result = crack.crack()

    def start_requests(self):
        # 如果本地cookie json文件不存在, 那么先进行自动化登录
        if not os.path.exists('tmp_data/xueqiu_cookie.json'):
            crack = CrackXueQiu()
            login_result = crack.crack()
            if not login_result:
                print('自动登录不成功，停止')
                pass

        with open('tmp_data/xueqiu_cookie.json', 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())

        expired = False
        # 检测token是否过期，如果过期，那么进行重新登录。
        for item in list_cookies:
            if item.get('expiry') and ('token' in item['name']):
                if time.time() > item.get('expiry'):
                    expired = True
                    break

        if expired:
            crack = CrackXueQiu()
            login_result = crack.crack()
            if not login_result:
                print('自动登录不成功，停止')
                pass

            with open('tmp_data/xueqiu_cookie.json', 'r', encoding='utf-8') as f:
                list_cookies = json.loads(f.read())

        cookies = [item["name"] + "=" + item["value"] for item in list_cookies]
        self.cookiestr = '; '.join(item for item in cookies)
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
        self.readSpecifySymbol = False
        self.symbols = ['ZH009248', 'ZH696958']
        if self.readSpecifySymbol:
            for s in self.symbols:
                yield scrapy.Request(f'{self.cube_profilt_url}{s}', self.parse_cube_profit_list, headers=self.send_headers)
                yield scrapy.Request(f'{self.cube_rebalance_url}{s}', self.parse_cube_rebalance_list,
                                     headers=self.send_headers, cb_kwargs=dict(symbol=s))
            pass
        else:
            # print(f'headers的内容是：{send_headers}')
            # print({cookiestr})
            current_page = 1
            final_url = f'{self.cube_discover_url}{current_page}'
            yield scrapy.Request(final_url, headers=self.send_headers)

    def parse_cube_profit_list(self, response):
        """
        解析组合列表数据，并存入h5文件
        :param response: 请求返回的json数组
        :return: None
        """
        if response.status == 200:
            json_response = json.loads(response.body_as_unicode())
            print('type of the result is1:' + str(len(json_response)))
            symbol = json_response[0]['symbol']

            h5name = f"cube_info_{symbol}.h5"
            self.hdf5.save_data_via_pandas(h5Name=h5name, key="profit_list", dataList=json_response[0]['list'])

    def parse_cube_rebalance_list(self, response, symbol):
        """
        解析调仓记录
        :param response:
        :param symbol:
        :return:
        """
        h5name = f"cube_info_{symbol}.h5"
        data_list = []
        if response.status == 200:
            json_response = json.loads(response.body_as_unicode())
            print(f'the raw response is {response}')
            print(f'the json response is {json_response}')
            page = json_response['page']
            max_page = json_response['maxPage']

            print(f'------------进行第{page}数据爬取')

            if page < max_page:
                page += 1
                self.cube_rebalance_url = f"https://xueqiu.com/cubes/rebalancing/history.json?count=20&page={page}&cube_symbol={symbol}"
                print(self.cube_rebalance_url)
                yield scrapy.Request(self.cube_rebalance_url, self.parse_cube_rebalance_list, headers=self.send_headers,
                                     cb_kwargs=dict(symbol=symbol), meta={"handle_httpstatus_all": True})

                self.hdf5.save_data_via_pandas(h5Name=h5name, key="rebalance_list", dataList=json_response['list'],
                                               exclude=['rebalancing_histories'])
                for history in json_response['list']:
                    data_list += history['rebalancing_histories']
        if data_list and len(data_list) > 0:
            self.hdf5.save_data_via_pandas(h5Name=h5name, key="rebalancing_histories", dataList=data_list, fillna=True)

    def parse(self, response):
        """
        雪球组合发现页面请求之后对内容进行解析
        :param response: 请求返回来的json字符串
        :return:
        """
        json_response = json.loads(response.body_as_unicode())

        for c in json_response['list']:
            loader = ItemLoader(item=CubeItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')

            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(c))
            item = loader.load_item()

            ownerloader = ItemLoader(item=OwnerItem())
            ownerloader.default_input_processor = MapCompose(str)
            ownerloader.default_output_processor = Join(' ')
            for (field, path) in self.owner_jmes_paths.items():
                ownerloader.add_value(field, SelectJmes(path)(c['owner']))
            owner = ownerloader.load_item()

            item['owner'] = owner
            yield item

            # 开始提取用户信息
            uid = owner['id']
            # https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid=6626771620&pid=-24（创建的组合）
            created_cube_url = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-24'
            #  请求用户创建的组合
            # 通过cb_kwargs的方式，给解析函数传递参数
            yield scrapy.Request(created_cube_url, self.parse_cube_list, headers=self.send_headers,
                                 cb_kwargs=dict(uid=uid, screen_name=owner['screen_name']))

            # 请求用户关注的组合，这个地方不去传递uid和screen_name信息，这种情况下，通过请求网页去解析，
            # TODO 请求网页的速度超慢，想办法优化，开启多线程？
            followed_cube_url = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-120'
            yield scrapy.Request(followed_cube_url, self.parse_cube_list, headers=self.send_headers)

            # 组合信息：
            # https://xueqiu.com/cubes/quote.json?code=ZH976766,SP1034535,SP1012810,ZH1160206,ZH2003755,ZH1996976,ZH1079481,ZH1174824,ZH1079472,SP1040320

        page = json_response['page']
        max_page = json_response['maxPage']
        if page < max_page:
            url = f'{self.cube_discover_url}{page + 1}'
            yield scrapy.Request(url, headers=self.send_headers)

    def parse_cube_list(self, response, uid=None, screen_name=None):
        """
        通过去查找创建的组合以及组合的基本信息
        :param response:
        :param uid:
        :param screen_name:
        :return:
        """
        json_response = json.loads(response.body_as_unicode())

        stock_json = json_response['data']['stocks']

        symbol_list_str = (",".join(str(s['symbol']) for s in stock_json))
        symbol_list = symbol_list_str.split(',')

        if uid is None:
            for s in symbol_list:
                yield scrapy.Request(f'{self.cube_info_url}{s}', self.parse_cube_detail_info, cb_kwargs=dict(symbol=s),
                                     headers=self.send_headers)
        else:
            cube_info_url = 'https://xueqiu.com/cubes/quote.json?code=' + symbol_list_str
            yield scrapy.Request(cube_info_url, self.parse_cube_info, headers=self.send_headers,
                                 cb_kwargs=dict(uid=uid, screen_name=screen_name, symbolList=symbol_list))

    def parse_cube_detail_info(self, response, symbol):
        """
        解析组合的详细详细信息
        :param response:
        :param symbol:
        :return:
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        uid = soup.find("a", {"class": "creator"})['href'][1:]
        screen_name = soup.find("div", {"class": "name"}).text
        symbol_list = [symbol]
        cube_info_url = 'https://xueqiu.com/cubes/quote.json?code=' + symbol
        yield scrapy.Request(cube_info_url, self.parse_cube_info, headers=self.send_headers,
                             cb_kwargs=dict(uid=uid, screen_name=screen_name, symbolList=symbol_list))

    def parse_cube_info(self, response, uid, screen_name, symbolList):
        json_response = json.loads(response.body_as_unicode())
        for s in symbolList:
            loader = ItemLoader(item=CubeItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')
            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(json_response[s]))
            item = loader.load_item()
            owner = OwnerItem()
            owner['id'] = uid
            owner['screen_name'] = screen_name
            item['owner'] = owner
            yield item
