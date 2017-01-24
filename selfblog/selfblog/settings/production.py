from .base import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('BLOG_DB_NAME'),
        'USER': get_env_variable('BLOG_DB_USER'),
        'PASSWORD': get_env_variable('BLOG_DB_PASSWORD'),
        'HOST': get_env_variable('BLOG_DB_HOST')
    }
}
