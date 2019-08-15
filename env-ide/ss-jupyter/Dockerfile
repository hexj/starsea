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
    locales git python-tk \ 
    # tk-dev libagg-dev python-matplotlib \ 
    # python-blosc libpng-dev libffi-dev dvipng texlive-latex-base \
    && locale-gen zh_CN.UTF-8 \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
    && echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen 
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

USER jovyan
COPY pip.conf /etc/pip.conf
COPY requirements.txt /home/jovyan/requirements.txt
# RUN pip install -U pip setuptools numpy cython 
# RUN pip install Cython git+https://github.com/rkern/line_profiler.git
# RUN pip install bcolz
RUN pip install -r /home/jovyan/requirements.txt
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
