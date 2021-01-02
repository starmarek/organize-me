ARG CORE_PYTHON_VER
FROM python:${CORE_PYTHON_VER}

WORKDIR /app

COPY Pipfile* ./

ARG CORE_PIPENV_VER
RUN pip install pipenv==${CORE_PIPENV_VER}
RUN pipenv sync
