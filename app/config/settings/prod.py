from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER' : env.str('DB_USER'),
        'PASSWORD' : env.str('DB_PASSWORD'),
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


PRIVATE_STORAGE_SERVER = 'nginx'
PRIVATE_STORAGE_INTERNAL_URL = '/media/'
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'media')