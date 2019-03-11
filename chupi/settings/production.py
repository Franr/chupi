from .base import *

INSTALLED_APPS += ("django_heroku",)

# Configure Django App for Heroku.
import django_heroku

django_heroku.settings(locals())
