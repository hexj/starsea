#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pandas.io.json import json_normalize
from collections import namedtuple

import pandas as pd
##############################################


class Json2Struct:
    ''' 
    Convert mappings to nested namedtuples 

    Usage: 
     jStruct = Json2Struct('JS').json2Struct(json) 
    '''
##############################################

    def __init__(self, name):
     self.namePrefix = name
     self.nameSuffix = 0

    def json2Struct(self, jsonObj):  # thank you https://gist.github.com/hangtwenty/5960435
     """ 
     Convert mappings to namedtuples recursively. 
     """
     if isinstance(jsonObj, Mapping):
      for key, value in list(jsonObj.items()):
       jsonObj[key] = self.json2Struct(value)
      return self.namedtuple_wrapper(**jsonObj)
     elif isinstance(jsonObj, list):
      return [self.json2Struct(item) for item in jsonObj]
     return jsonObj

    def namedtuple_wrapper(self, **kwargs):
     self.nameSuffix += 1
     name = self.namePrefix + str(self.nameSuffix)

     Jstruct = namedtuple(name, kwargs)
     globals()[name] = Jstruct

     return Jstruct(**kwargs)

def main():
    jsonfile = 'history.json'
    data_str = open(jsonfile).read()

    # x = json.loads(data_str, object_hook=lambda d: namedtuple('Page', d.keys())(*d.values()))
    page = Json2Struct('Page').json2Struct(data_str)
    print(page.list)

    # data_list = json.loads(data_str)
    # print(type(data_list['list']))
    print("-=-=-=-=-=-=-")

    # df = json_normalize(data_list)
    # df = json_normalize(data_list['list'])
    # print(df)
    pass

def _time_analyze_(func):
    import time
    t1_start = time.perf_counter()
    func()
    t1_stop = time.perf_counter()
    print("Elapsed time: %s s" % (t1_stop - t1_start))


if __name__ == '__main__':
    _time_analyze_(main)
