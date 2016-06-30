"""
Django settings for swipe project.

======================
DO NOT EDIT THIS FILE!
======================
Copy the settings you want to change to your local.py file and change them there!
"""

import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse_lazy



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(&-^3hx6os!h^sxu(v2py(78zuqtp8pxtu_3f=jh$+c4hw1taw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = (
    # django stuff
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',

    # utilities
    'compressor',
    'compressor_toolkit',

    # our apps
    'core',
    'www',
    'money',
    'supplier',
    'crm',
    'register',
    'article',
    'stock',
    'assortment',
    'tools',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'swipe.urls'

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
                'tools.context_preprocessors.swipe_globals',
            ],
        },
    },
]

WSGI_APPLICATION = 'swipe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Default logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s %(funcName)s (%(filename)s:%(lineno)d) %(message)s',
        },
    },
    'handlers': {
        # File handler, uncomment and add to loggers to log to file
        # 'swipe-file': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.WatchedFileHandler',
        #     'filename': '/tmp/swipe-production.log',
        #     'formatter': 'verbose',
        # },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {  # all other errors go to the console
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'swipe': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    },
}

# LDAP Settings, please set these in the local.py if you want to use LDAP.
AUTH_LDAP_SERVER_URI = "LDAP_URL"
AUTH_LDAP_BIND_DN = "BIND_DN"
AUTH_LDAP_BIND_PASSWORD = "LDAP_USER_PASSWORD"
AUTH_LDAP_USER_SEARCH = None
AUTH_LDAP_GROUP_SEARCH = None
AUTH_LDAP_GROUP_TYPE = None
AUTH_LDAP_REQUIRE_GROUP = "REQUIRE_GROUP"
AUTH_LDAP_USER_ATTR_MAP = {}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {}
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Login paths
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# How to generate locale files:
# https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#localization-how-to-create-language-files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = []

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
)

COMPRESS_NODE_MODULES = os.path.join(BASE_DIR, 'node_modules')

COMPRESS_SCSS_COMPILER_CMD = (
    'node-sass --output-style expanded {paths} "{infile}" "{outfile}" && '
    'postcss --use "{node_modules}/autoprefixer" '
    '--autoprefixer.browsers "{autoprefixer_browsers}" -r "{outfile}"'
)

COMPRESS_ES6_COMPILER_CMD = (
    'export NODE_PATH="{paths}" && '
    'browserify "{infile}" -o "{outfile}" --full-paths ' +
    ('-d ' if DEBUG else '') +
    '-t [ babelify '
    '--presets [ es2016 ] ]'
)


##
# SWIPE SETTINGS
##
# Add new settings for swipe modules here.
##

# Monetary precision. Don't change unless you know what you're doing.
DECIMAL_PLACES = 5
MAX_DIGITS = 28

#Should swipe delete stocklines at count zero?
DELETE_STOCK_ZERO_LINES = True

# Should swipe's stock model throw an error when the software attempts to remove stock at a different price from the stock on stock? Sensible: True
FORCE_NEGATIVE_STOCKCHANGES_TO_MAINTAIN_COST = True

# Name of cash payment type
CASH_PAYMENT_TYPE_NAME = "Cash"

# Current currency. Transactions are only possible with this currency
USED_CURRENCY = "EUR"

SWIPE_JS_GLOBAL_VARS = {
    'api': {
        'assortment': reverse_lazy('api.assortment'),
    },
}

##
# WARNING: Add own settings ABOVE this comment.
# The following lines are to load local settings.
##

# Import local user settings from local.py
try:
    from swipe.local import *
except ImportError:
    print("WARNING: You forgot to add your local settings. "
          "Please copy local.py.default to local.py in the swipe directory and change it to fit your needs.")
