FROM python:3.9.1-buster

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv sync
