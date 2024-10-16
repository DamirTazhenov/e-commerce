from config.settings.base import *
import json

DEBUG = True if os.environ.get('DJANGO_DEBUG_STAGE') == 'True' else False


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = json.loads(os.environ.get('ALLOWED_HOSTS'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB_STAGE'),
        'USER': os.environ.get('POSTGRES_USER_STAGE'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_STAGE'),
        'HOST': os.environ.get('POSTGRES_HOST_STAGE'),
        'PORT': os.environ.get('POSTGRES_PORT_STAGE'),
    }
}

REDIS_HOST = os.environ.get('REDIS_HOST_STAGE')
REDIS_PORT = os.environ.get('REDIS_PORT_STAGE')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': False,  # Use this to avoid errors if Redis is down
        }
    }
}

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'