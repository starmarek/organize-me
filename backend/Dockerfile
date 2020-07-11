# pull official base image
FROM python:3.6-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN apt update -yq && apt install libpq-dev -y
COPY Pipfile* ./
RUN pipenv install --ignore-pipfile
