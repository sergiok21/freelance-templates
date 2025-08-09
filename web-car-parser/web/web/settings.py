import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '...'

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [...]


CSRF_TRUSTED_ORIGINS = [
    f'{os.environ.get("MAIN_URL")}',
]


INSTALLED_APPS = [
    'jazzmin',
    'axes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',

    'interface'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'axes.middleware.AxesMiddleware',
    'interface.middlewares.LogIPMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'interface.backends.TokenBackend',
]

SESSION_SAVE_EVERY_REQUEST = True


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

APPEND_SLASH = True


STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = BASE_DIR / 'static/'


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Locales
LOCALE_PATHS = (BASE_DIR / 'locale', )
LANGUAGES = (
    ('en', _('English')),
    ('sl', _('Slovenian')),
    ('ru', _('Russian')),
)


# REST
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}


# Axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(hours=6)
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_USE_USER_AGENT = True
AXES_BEHIND_REVERSE_PROXY = True
AXES_CLIENT_IP_ATTRIBUTE = 'HTTP_X_FORWARDED_FOR'
AXES_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR'
]


# Headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Logger
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        ct += timedelta(hours=3)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s

    def apply_config(self, configs: list) -> list:
        processed_handlers = []
        for item in configs:
            item[0].setLevel(item[1])
            item[0].setFormatter(self)
            processed_handlers.append(item[0])
        return processed_handlers


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

formatter_obj = CustomFormatter(
    fmt='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

warning_handler, critical_handler, general_handler = \
    logging.StreamHandler(), logging.StreamHandler(), logging.StreamHandler()

handlers_config = [
    [warning_handler, logging.WARNING], [critical_handler, logging.CRITICAL], [general_handler, logging.INFO]
]

logging.basicConfig(level=logging.DEBUG, handlers=formatter_obj.apply_config(configs=handlers_config))
