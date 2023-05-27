from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[DjangoIntegration()])

CACHES["default"]["LOCATION"] = os.getenv("REDIS_URL")
CACHES["default"]["KEY_PREFIX"] = "prod"


DATABASES["default"] = {
    "ENGINE": "django_psdb_engine",
    "NAME": os.getenv("DB_NAME"),
    "USER": os.getenv("DB_USERNAME"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
    "HOST": os.getenv("DB_HOST"),
}
