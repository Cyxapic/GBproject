### GBproject ###

# Geek Brains study project - blog #

# DEVELOPMENT MINIMAL SETTINGS: #
- pip install -r requirements.txt
- file name: development.py
- don't forget to create 'secrets.json'
    - minimal {"NAME": "", "USER": "", "PASSWORD": "", "SECRET_KEY": "NOT A SECRET"}

```
import os

from .base import BASE_DIR


DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```