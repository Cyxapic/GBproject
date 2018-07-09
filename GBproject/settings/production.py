from django_secrecy.utils import get_secret

from .base import BASE_DIR


DEBUG = False

ALLOWED_HOSTS = ['*']

# Default MySql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret(BASE_DIR, 'NAME'),
        'USER': get_secret(BASE_DIR, 'USER'),
        'PASSWORD': get_secret(BASE_DIR, 'PASSWORD'),
        'HOST': '',
        'PORT': '',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_unicode_ci'
        }
    }
}
