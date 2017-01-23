from .base import *


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djblog',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1'
    }
}

