FROM python:3.6.12-buster

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv sync
