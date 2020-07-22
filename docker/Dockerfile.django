FROM python:3.6-slim-buster

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . .
RUN pipenv sync
