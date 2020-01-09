import numpy as np
import h5py
import json
import pandas as pd
import scrapy
import logging

logger = logging.getLogger(__name__)


class Hdf5Utils(object):
    def save_data_via_pandas(self, h5_name, key, data_list, columns=None):
        '''
        h5Name: hdf5文件命令
        key：对应 hdf5文件里面的group
        exclude：是否exclude某些属性
        fillna：对于Null的数据，是否进行填充;如果某一次假如的数据全为null，之后加入的数据类型，有可能会出现类型不匹配的情况。
        '''
        # 需要把Null的数据设置为0.0 否则会出现append的时候，类型不匹配的问题
        # if fillna:
        #     profit_list_item = pd.DataFrame.from_records(data_list, exclude=exclude, coerce_float=True).fillna(0.0)
        # else:
        #     profit_list_item = pd.DataFrame.from_records(data_list, exclude=exclude, coerce_float=True)

        if columns:
            profit_list_item = pd.DataFrame(data_list, columns=columns)
        else:
            profit_list_item = pd.DataFrame(data_list)

        try:
            # profit_list_item.to_hdf(f'db_data/{h5_name}', format='table', key=key, mode='a', append=True, complevel=9)
            logger.warning(profit_list_item.dtypes)

            store = pd.HDFStore(f'db_data/{h5_name}', mode='a')
            store.append(key, profit_list_item)
            store.close()
        except Exception as e:
            logger.error(profit_list_item.dtypes)
            logger.error(e)


    def read_data_from_hdf5(self, h5_name, key):
        '''
        读取整个H5文件的内容，返回值是一个DataFrame
        '''
        return pd.read_hdf(h5_name, key=key)

    def query_data_from_hdf5(self, h5_name, key, query):
        '''
        通过query条件从H5文件查询内容，返回值是一个DataFrame
        '''
        return pd.read_hdf(h5_name, key=key).query(query)
