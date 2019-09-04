ARG BASE_CONTAINER=jupyter/base-notebook
FROM $BASE_CONTAINER

# RUN sudo cp /etc/apt/sources.list sources.list_backup
COPY source.list /etc/apt/sources.list

# RUN whoami
USER root
# MPLBACKEND=TkAgg
RUN echo "DEBIAN_FRONTEND noninteractive\nLC_ALL=zh_CN.UTF-8\nLANG=zh_CN.UTF-8\nLANGUAGE=zh_CN.UTF-8\n" >> /etc/environment \
    && apt-get update --fix-missing && apt-get upgrade -y \
    && apt-get install -y apt-utils make gcc fonts-humor-sans \
    locales git python-tk cmake build-essential \ 
    # tk-dev libagg-dev python-matplotlib \ 
    # python-blosc libpng-dev libffi-dev dvipng texlive-latex-base \
    && locale-gen zh_CN.UTF-8 \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
    && echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && wget -O /usr/share/fonts/SimHei.ttf "https://github.com/hexj/bin-file/raw/master/fonts/SimHei.ttf"

RUN apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm -rf /home/jovyan/.cache/matplotlib/

RUN wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz \
    && tar xvf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib \
    && rm ta-lib-0.4.0-src.tar.gz

# RUN cd /app  && git clone https://github.com/PAIR-code/facets 
ADD deps/facets /app/facets/
RUN cd /app/facets/facets_dive \
    && cd /app/facets/facets_dive && jupyter nbextension install /app/facets/facets-dist/ 
    # && cd /app/facets/facets_dive

ADD deps/libtaos.so /usr/lib64 
ADD deps/taos-py3 /app/taos-py3/
RUN pip install /app/taos-py3/ 
# ADD deps/taos.cfg /etc/taos/
# RUN cd /app/TDengine/ && cmake ../TDengine && cmake --build . \ 
#     && cp /app/TDengine/build/bin/* /app/ \
#     && cp /app/TDengine/build/lib/libtaos.so /usr/lib64 \
#     && pip install /app/TDengine/src/connector/python/linux/python3/ \
#     && ldconfig

USER jovyan
COPY pip.conf /etc/pip.conf
COPY requirements.txt /home/jovyan/requirements.txt
# RUN pip install -U pip setuptools numpy cython 
# RUN pip install Cython git+https://github.com/rkern/line_profiler.git
# RUN pip install bcolz
RUN pip install jupyter_contrib_nbextensions jupyter_nbextensions_configurator \
    && jupyter nbextensions_configurator enable --user \
    && jupyter contrib nbextension install --user \
    && pip install -r /home/jovyan/requirements.txt \
    && echo "c.NotebookApp.iopub_data_rate_limit = 1000000000" >> ~/.jupyter/jupyter_notebook_config.py 


# RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager \
#     && pip install jupyter_contrib_nbextensions jupyter_nbextensions_configurator \
#     && jupyter contrib nbextension install --user
#     && jupyter nbextensions_configurator enable --user
#     && jupyter labextension install jupyter-matplotlib \
#     && jupyter nbextension enable --py widgetsnbextension \
#     && jupyter serverextension enable --py jupyterlab

# RUN mkdir -p /home/jovyan/.config/matplotlib \
#     && echo "backend: TkAgg" >> ~/.config/matplotlib/matplotlibrc \
# && pip install -r /home/jovyan/ss/requirements.txt \
# && jt -t onedork -f roboto -fs 14 -nfs 14 -tfs 14 -ofs 11
#jt -t oceans16 -T -N
