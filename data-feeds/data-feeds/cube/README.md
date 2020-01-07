cube: 组合数据，目前数据源有雪球组合

首先拷贝cube_settings_copy.py文件，然后重命名为cube_settings.py，并填入雪球账号密码，
ps: 因为cube_settings.py已经加到gitignore文件中，所以不用担心账号密码会被提交到github

本项目使用的虚拟环境工具为pipenv, 通过pip install pipenv进行安装，安装完成之后，根据自己的开发环境进行启动，启动方法如下：

### VS Code环境中使用pipenv
直接通过VS Code里面的terminal工具，进入到cube目录，执行 pipenv shell，即可进入到pipenv虚拟环境，指定pipenv sync


### Pycharm
通过terminal, cd 到data-feeds/cube目录下，执行pipenv shell 和 pipenv sync（同VS Code中terminal的使用)
关于Pychar中指定python解释器，可以直接参考[这里](https://blog.csdn.net/qq_20728575/article/details/82949529)
在pycharm指定解释器为pipenv之后，直接运行main.py即可

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

