FROM python:3.6-slim-buster

WORKDIR /usr/src/app

# flush python logs immediately; do not buffer
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv
# libpq-dev is a debian-base dependency for psycopg2-binary
RUN apt update -yq && apt install libpq-dev -y

COPY Pipfile* ./
RUN pipenv sync
