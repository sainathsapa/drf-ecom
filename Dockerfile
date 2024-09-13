FROM python:3


RUN apt-get update
# RUN apt-get install python3 python3-pip -y
RUN apt-get install -y cron
# RUN apt-get install gunicorn3 -y

WORKDIR /web-app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

# COPY ./ ./



