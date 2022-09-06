FROM ubuntu:20.04

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Project files and settings
RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3-pip
RUN python3.9 -m pip install pipenv -y

RUN mkdir /app
COPY . /app/

WORKDIR /app

RUN pipenv install --deploy --system

CMD ["python"]