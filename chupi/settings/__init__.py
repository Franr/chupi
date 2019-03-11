import os

if "HEROKU" in os.environ:
    from chupi.settings.production import *
else:
    from chupi.settings.base import *
