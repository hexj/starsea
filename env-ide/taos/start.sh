#! /bin/bash
if [ ! -d "TDengine" ]; then
  git clone https://github.com/taosdata/TDengine.git
fi
cd TDengine
git pull
cd ..
# pip install TDengine/src/connector/python/linux/python3
docker system prune -f
docker-compose up 
