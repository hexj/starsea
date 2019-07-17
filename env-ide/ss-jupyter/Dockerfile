ARG BASE_CONTAINER=jupyter/base-notebook
FROM $BASE_CONTAINER

# for mirrors in China
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
COPY pip.conf /root/.pip/pip.conf

COPY source.list /etc/apt/sources.list
RUN whoami
USER root
RUN sudo cp /etc/apt/sources.list sources.list_backup
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y apt-utils locales git \
    && locale-gen zh_CN.UTF-8 \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
    && echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment
USER jovyan
RUN git clone https://github.com/hexj/starsea \
    && cd starsea \
    && pip install -r env-ide/ss-jupyter/requirements.txt \
    # && pip install -r /requirements.txt \
    && pip install -e . \
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8