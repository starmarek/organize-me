FROM python:3.6-slim-buster

WORKDIR /app

RUN apt update && apt install netcat -y
RUN pip install --upgrade pip
RUN pip install pipenv

COPY . .
RUN pipenv sync
