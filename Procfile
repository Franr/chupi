release: python manage.py migrate --noinput
web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn chupi.wsgi
