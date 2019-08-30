### 说明
这个目录下主要是练习**funcat**的使用

### Plans
- []funcat的安装和demo初步实践
- []寻找一些实际场景的使用，加深funcat的理解和使用
- [] 阅读一下funcat的源码

### 遇到的问题：

#### 1. (Ubuntu) 安装的时候，因为我本地没有安装ta-lib，导致安装失败

首先需要安装[ta-lib](https://github.com/mrjbq7/ta-lib), 这个类库是基于Python对[TA-Lib](http://ta-lib.org/)的封装，具体环境的的问题，可以看[ta-lib](https://github.com/mrjbq7/ta-lib) readme里面的Troubleshooting章节

#### 2. (Ubuntu) [Rqalpha](https://github.com/ricequant/rqalpha)安装完成之后，运行的时候，发生了如下错误 
```
bundle path /home/weibolei/.rqalpha/bundle not exist
```
安装完Rqalpha之后，需要执行rqalpha update-bundle

#### 3. (Ubuntu) 安装完bundle之后，运行的时候出现下面错误：
```
TypeError: __init__() missing 1 required positional argument: 'price_board'
```
##### 非常规做法
rqalpha 降到3.2.0 同时修改本地库中下面这个文件
/usr/local/lib/python3.6/dist-packages/rqalpha/model/instrument.py
修改为：
```
    def _fix_date(ds, dflt):
        if ds == '0000-00-00':
            return dflt
        #print(str(type(ds)) + '--->' + str(ds))
        if isinstance(ds, datetime.datetime):
            year = ds.strftime('%Y')
            month = ds.strftime('%m')
            day = ds.strftime('%d')
            #print(day)
        else: 
            year, month, day = str(ds).split('-')
        return datetime.datetime(int(year), int(month), int(day))
```

##### 其他方案？？？？？