import sentry_sdk

from .base import *

INSTALLED_APPS += ("django_heroku",)

# Configure Django App for Heroku.
import django_heroku

django_heroku.settings(locals())

from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], integrations=[DjangoIntegration()])

REDIS_URL = os.environ.get("REDIS_URL")
