FROM python:3.8-slim-buster

# working dir
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y

# environment variable
# no pyc
ENV PYTHONDONTWRITEBYTECODE 1 
# no log
ENV PYTHONBUFFERED 1

COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt