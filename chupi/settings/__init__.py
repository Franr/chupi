import os

if "PROD" in os.environ:
    from chupi.settings.production import *
else:
    from chupi.settings.base import *
