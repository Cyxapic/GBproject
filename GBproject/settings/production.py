from .base import secrets


DEBUG = False
# CHANGE '*' - on your domain names
ALLOWED_HOSTS = ['dev.cyxapic.ru']

# Default MySql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets.NAME,
        'USER': secrets.USER,
        'PASSWORD': secrets.PASSWORD,
        'HOST': '',
        'PORT': '',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_unicode_ci'
        }
    }
}

EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_PORT = secrets.EMAIL_PORT
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = secrets.EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = secrets.DEFAULT_FROM_EMAIL
