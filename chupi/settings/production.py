from .base import *

INSTALLED_APPS += ("django-heroku",)

# Configure Django App for Heroku.
import django_heroku

django_heroku.settings(locals())
