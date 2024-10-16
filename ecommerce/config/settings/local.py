from config.settings.base import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB_LOCAL'),
        'USER': os.environ.get('POSTGRES_USER_LOCAL'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_LOCAL'),
        'HOST': os.environ.get('POSTGRES_HOST_LOCAL'),
        'PORT': os.environ.get('POSTGRES_PORT_LOCAL'),
    }
}

REDIS_HOST = os.environ.get('REDIS_HOST_LOCAL')
REDIS_PORT = os.environ.get('REDIS_PORT_LOCAL')

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