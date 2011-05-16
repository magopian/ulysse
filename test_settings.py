# Django settings for scratch project.

import os
from settings import *

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test.db'),
    },
}

