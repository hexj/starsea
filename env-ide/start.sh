#! /bin/bash

echo "当前执行文件......$0"
function docker_install()
{
	echo "检查Docker......"
	docker -v
    if [ $? -eq  0 ]; then
        echo "检查到Docker已安装!"
    else
    	echo "请安装docker环境..."
        echo "mac 环境 url https://download.docker.com/mac/stable/Docker.dmg"
        echo "windows 环境请访问 https://download.docker.com/win/static/stable/x86_64/"
        # curl -sSL https://get.daocloud.io/docker | sh
        # echo "安装docker环境...安装完成!"
    fi
    # 创建公用网络==bridge模式
    #docker network create starsea_network
}
function gettdengine(){
    cd taos
    if [ ! -d "TDengine" ]; then
        git clone https://github.com/taosdata/TDengine.git
    fi
    cd TDengine
    git pull
    cd ../..
}
function getfacet()
{   
    cd ss-jupyter/deps
    if [ ! -d "facets" ]; then
        git clone https://github.com/PAIR-code/facets
    fi
    cd facets
    git pull
    cd ../../../
}
function getlibtaos(){
    if [ ! -f "ss-jupyter/deps/libtaos.so" ]; then
        echo "get libtaos"
        wget -P ss-jupyter/deps/ https://github.com/2efPer/tdengine-docker/raw/master/spark-app/libtaos.so
    fi
}
function getfont(){
    if [ ! -f "ss-jupyter/deps/SimHei.ttf" ]; then
        echo "get font"
        wget -P ss-jupyter/deps/ https://github.com/hexj/bin-file/raw/master/fonts/SimHei.ttf
    fi
}
function gettalib(){
    if [ ! -f "ss-jupyter/deps/ta-lib-0.4.0-src.tar.gz" ]; then
        echo "get talib"
        wget -P ss-jupyter/deps/ https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
    fi
}
function main(){
    # 执行函数
    docker_install
    {
        gettdengine
    } &

    {
        getfacet
    } &
    {
        getfont
    } &
    {
        gettalib
    } &
    {
        docker pull mysql
    } &
    {
        getlibtaos
    } &
    wait
    # docker-compose build 
    docker system prune -f
    

    cp -r taos/TDengine/src/connector/python/linux/python3 ss-jupyter/deps/taos-py3
    docker-compose up # --build
    # docker logs starsea 2>&1 | grep "token" | grep -v "NotebookApp"
}

main
