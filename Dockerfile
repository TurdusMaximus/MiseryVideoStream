FROM python:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-pip -y
RUN apt-get install ffmpeg -y

COPY . /py
WORKDIR /py

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 -m bot
