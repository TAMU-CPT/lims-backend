import os
import datetime
import random
import string

if not os.path.exists('/tmp/django_secret'):
    with open('/tmp/django_secret', 'w') as handle:
        handle.write("".join([random.SystemRandom().choice(string.digits + string.punctuation) for i in range(100)]))

with open('/tmp/django_secret', 'r') as handle:
    SECRET_KEY = handle.read()


DEBUG = os.environ.get('DJANGO_DEBUG', None) == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGINS', '').split(',')

import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://d99e2548365547a5be096a19a0a976d4:32215ddb805d48a98ca5f4658e6fb339@cptgnome.tamu.edu/12',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

STATIC_URL = '/%sstatic/' % os.environ.get('DJANGO_URL_PREFIX', '')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
