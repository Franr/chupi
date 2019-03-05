FROM python:3.7-alpine

MAINTAINER Francisco Rivera

ENV PYTHONUNBUFFERED 1

# Creating working directory

COPY . /code
WORKDIR /code

# Prepare dependencies

RUN apk add --no-cache bash \
    && pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile

# Run server

CMD ./manage.py runserver 0.0.0.0:8000
