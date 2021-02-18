#!/usr/bin/env sh
echo "Waiting for postgres..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"
pipenv run python manage.py migrate
pipenv run python manage.py runserver 0:8000
