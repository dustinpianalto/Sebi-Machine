FROM ubuntu:latest
ENV LC_ALL C
MAINTAINER PUFFDIP

ADD . /bot
WORKDIR /bot
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install python3.6 && \
    apt-get install python3-pip -y
RUN apt install git -y
RUN python3.6 -m pip install --upgrade pip && \
    python3.6 -m pip install -r requirements.txt && \
    python3.6 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

cmd ["python3.6","-m","src"]
