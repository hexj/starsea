FROM selenium/standalone-chrome

# install python3
USER root
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean
RUN apt-get update && apt-get install -y python3.7 python3-pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.7 get-pip.py
RUN pip --version

RUN python3.7 --version
RUN cd ~

# install requirement
COPY ./requirements.txt ./requirements.txt
RUN ls
RUN pip install -r requirements.txt
RUN chromedriver --version
RUN google-chrome --version


# set display port to avoid crash
ENV DISPLAY=:99