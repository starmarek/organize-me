""" Production Settings """

import os
import dj_database_url
from .dev import *

############
# DATABASE #
############
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}


############
# SECURITY #
############

DEBUG = bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# The '*' is an official Heroku config. Refer to:
# https://devcenter.heroku.com/articles/django-app-configuration
# https://github.com/heroku/django-heroku
ALLOWED_HOSTS = ['*']
