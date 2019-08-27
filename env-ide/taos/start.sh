#! /bin/bash
if [ ! -d "TDengine" ]; then
  git clone https://github.com/taosdata/TDengine.git
fi
cd TDengine
git pull
cd ..
#linux/ mac 中如需要用 python 访问该数据 需要从源码安装依赖
# pip install TDengine/src/connector/python/linux/python3
docker system prune -f
docker-compose up 

#docker exec -it taos /bin/bash 
#/app# ./taos