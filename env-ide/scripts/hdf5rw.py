#!/usr/bin/env python
# -*- coding: utf-8 -*-
import h5py  #导入工具包
import numpy as np

def rwtst():
    #HDF5的写入：
    imgData = np.zeros((30,3,128,256))
    f = h5py.File('HDF5_FILE.h5','w')   #创建一个h5文件，文件指针是f
    f['data'] = imgData                 #将数据写入文件的主键data下面
    f['labels'] = range(100)            #将数据写入文件的主键labels下面
    f.close()                           #关闭文件
    
    #HDF5的读取：
    with h5py.File('HDF5_FILE.h5','r') as f:
        f.keys()                            #可以查看所有的主键
        a = f['data'][:]                    #取出主键为data的所有的键值
        print(a)


# def print_attrs(name, obj):
#     print(name)
#     items = obj.attrs.items()
#     for key, val in items:
#         print("%s=%s" % (key, val))
#     pass
def rwgroup():
    fname = "cube_info_ZH009248.h5"
    with h5py.File(fname, 'r') as f:
        # f.visititems(print_attrs)
        for key in f.keys():
            print(key)
            items = f[key].attrs.items()
            for key,val in items :
                print("%s=%s"%(key,val))
            print("-=-=-=-=-=-=-=-=-=-=-")
            # print(f[key].attrs.items())

def main():
    rwgroup()


def _time_analyze_(func):
    import time
    t1_start = time.perf_counter()
    func()
    t1_stop = time.perf_counter()
    print("Elapsed time: %s s" % (t1_stop - t1_start))


if __name__ == '__main__':
    _time_analyze_(main)
