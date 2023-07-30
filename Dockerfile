FROM python:3.11.4-slim-bookworm

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean

RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install libmagic1 -y && \
    apt-get clean

#RUN mkdir -p /app/{src,tests}
RUN mkdir -p /app/src
COPY src /app/src
#COPY tests /app/tests
COPY LICENSE README.md requirements.txt setup.cfg setup.py /app/

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python setup.py install