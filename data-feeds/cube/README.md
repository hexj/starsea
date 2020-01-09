cube: 组合数据，目前数据源有雪球组合

首先拷贝在cube/config目录下，拷贝一份cube_settings_copy.py文件重命名为cube_settings.py，并填入雪球账号密码，

**ps: 由于cube_settings.py已经加到gitignore文件中，所以不用担心账号密码会被提交到github**

默认chromedriver起来的浏览器添加了--headerless, 如果需要调出chromedriver的页面，请在cube/crack/xueqiu_login.py里面将headless
和 disable-gpu注释。如果需要将爬虫的日志打印到文件，修改cube/setttings.py将
`# LOG_FILE = log_file_path` 这行注释放开，默认LogLevel设置为debug，可以根据自己的需求修改等级。

## Docker环境运行
在当前目录下直接执行 docker-compose up即可

##开发环境搭建
项目使用的虚拟环境工具为pipenv, 通过pip install pipenv进行安装，安装完成之后，根据自己的开发环境进行启动，启动方法如下：

首次运行项目需要, 执行pipenv shell,然后执行pipenv sync安装依赖。

### VS Code
导入项目到vscode, 可以安装python插件，也可以直接通过命令行运行
```python
python main.py
```

### Pycharm
Pycharm导入到项目，然后，Pycharm指定Python解释器
关于Pycharm中指定python解释器，可以直接参考[这里](https://blog.csdn.net/qq_20728575/article/details/82949529)
在pPycharm指定解释器为pipenv之后，直接运行main.py即可



## 关于pipenv使用的一点说明
### pipenv 修改加速镜像
```
[[source]]
url = "https://pypi.doubanio.com/simple"
verify_ssl = true
name = "douban"
```

### 生成requirements.txt文件
```
$ pipenv lock -r
```

#### 生成dev-packages的requirements.txt文件
```
$ pipenv lock -r -d
```

更多关于pipenv的使用，可以参考[这里](https://stornado.github.io/2019/01/23/pipenv-in-pratical/)

