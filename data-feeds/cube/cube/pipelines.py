# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import redis
from cube.items import CubeItem, CubeProfitItem, CubeRebalanceItem, CubeRebalanceHistoryItem
from cube.spiders.hdf5 import Hdf5Utils
from cube.models.cube_profit_wrapper import cube_profit_wrapper_to_dict
from cube.models.cube_rebalancing_history_item_wrapper import cube_rebalance_history_item_wrapper_to_dict
from cube.models.cube_rebalancing_item_wrapper import cube_rebalance_item_wrapper_to_dict



class CubePipeline(object):
    cube_list = []
    cube_list_h5_name = "cube_list.h5"
    cube_list_h5_key = "cube_list"

    def __init__(self):
        self.hdf5 = Hdf5Utils()

    def process_item(self, item, spider):
        if isinstance(item, CubeItem):
            self.cube_list.append(item['data_item'].to_dict())
            if len(self.cube_list) >= 100:
                self.save_cube_list()

        elif isinstance(item, CubeProfitItem):
            h5name = f"cube_info_{item['symbol']}.h5"
            data_list = cube_profit_wrapper_to_dict(item['data_list'])
            self.hdf5.save_data_via_pandas(h5_name=h5name, key="profit_list", data_list=data_list)

        elif isinstance(item, CubeRebalanceItem):
            h5name = f"cube_info_{item['symbol']}.h5"
            data_list = cube_rebalance_item_wrapper_to_dict(item['data_list'])
            # 正常rebalance_list包含rebalancing__histories的内容，但是因为hdf5通过pd去存储，不能内部对象结构
            # 因此这里拆成两个存储
            self.hdf5.save_data_via_pandas(h5_name=h5name, key="rebalancing_list", data_list=data_list)

        elif isinstance(item, CubeRebalanceHistoryItem):
            h5name = f"cube_info_{item['symbol']}.h5"
            data_list = cube_rebalance_history_item_wrapper_to_dict(item['data_list'])
            # 正常rebalance_list包含rebalancing__histories的内容，但是因为hdf5通过pd去存储，不能内部对象结构
            # 因此这里拆成两个存储
            self.hdf5.save_data_via_pandas(h5_name=h5name, key="rebalancing_histories", data_list=data_list)
        return item

    def save_cube_list(self):
        """
        保存组合列表，这个方法在后面close的时候，还需要用到，所以这里抽象出一个方法
        :return:
        """
        self.hdf5.save_data_via_pandas(h5_name=self.cube_list_h5_name, key=self.cube_list_h5_key,
                                       data_list=self.cube_list)
        self.cube_list.clear()
        pass

    def close_spider(self, spider):
        """
        爬虫结束
        :param spider:
        :return:
        """
        self.save_cube_list()
