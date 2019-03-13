FROM python:3.7-alpine

MAINTAINER Francisco Rivera

ENV PYTHONUNBUFFERED 1

# Creating working directory

COPY . /code
WORKDIR /code

# Prepare dependencies

RUN \
    apk add --no-cache postgresql-libs bash && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev linux-headers && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    apk --purge del .build-deps

# Run server

CMD ./manage.py runserver 0.0.0.0:8000
