USE_POSTGRESS = False

DEBUG = True
LOCAL = True

#
# sqlite database for dev
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

#
# Local postgres
#
if USE_POSTGRESS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # Or path to database file if using sqlite3.
            'NAME': 'videopath_import',
            'USER': '',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

#
# Unclear why this is needed
#
INTERNAL_IPS = ('127.0.0.1',)

#
# Setup Logging
#
import logging
LOGGER = logging.getLogger('videopath')

import sys
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'videopath': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#
# Different invoice start number
#
INVOICE_START_NUMBER = 49

#
# Stripe dev key
#
STRIPE_API_KEY = ""

#
# Amazon Keys
#
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_PIPELINE_ID = ''

#
# Mandrill key
#
MANDRILL_APIKEY = ''

#
# Mailchimp key
#
MAILCHIMP_APIKEY = ""

#
# GA
#
GA_PASSWORD = ''

#
# Set dev player locations
#
AWS_PLAYER_BUCKET = "player-dev.videopath.com"
PLAYER_SRC = '//player-dev.videopath.com/develop/'
PLAYER_LOCATION = 'http://player-dev.videopath.com/'

#
# Integrations
#
MAILCHIMP_CLIENT_ID = ""
MAILCHIMP_CLIENT_SECRET = ""

#
# Sendgrid
#
SENDGRID_API_KEY = ""
