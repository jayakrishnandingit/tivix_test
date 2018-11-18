# flake8: noqa
from .base import *


PRODUCTION = False
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'HOST': os.environ['POSTGRES_HOST'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}

print('SECRET_KEY', SECRET_KEY)
print('SETTINGS', os.environ['DJANGO_SETTINGS_MODULE'])
