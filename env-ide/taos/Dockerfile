FROM ubuntu AS build-env

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && apt-get -y install git \
    && apt-get -y install build-essential \
    && apt-get -y install cmake \
    && pwd

WORKDIR /app
# RUN git clone https://github.com/taosdata/TDengine.git
ADD TDengine /app/TDengine/
RUN mkdir build && cd build && cmake ../TDengine && cmake --build . && pwd && ls /app/build/build/bin 

FROM ubuntu
WORKDIR /app
# COPY --from=build-env /TDengine/* /app/src/
COPY --from=build-env /app/build/build/bin/* /app/
# RUN cp /app/build/build/bin/* /app/
RUN mkdir -p /data/log
# ENTRYPOINT ["./taosd", "-c", "/etc/taos/"]
