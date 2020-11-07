# Django settings for videopath project.
import os


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*.videopath.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
# STATICFILES_DIRS = (
#     os.path.join(SITE_ROOT, 'static'),
# )

# make commons middleware append a slash to urls
APPEND_SLASH = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a7re2_u(e^h3^gqd1s*4if^tc@ie=9867ip_0#ik7ck0jyd4+_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'videopath.middleware.corsheader.CorsHeaderMiddleware',
    'videopath.middleware.maintenance_mode.MaintenanceModeMiddleware',
    'videopath.middleware.token_auth.TokenAuthMiddleware',
    'videopath.apps.users.middleware.manipulate_path.ManipulatePathMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'videopath.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'videopath.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

GRAPPELLI_ADMIN_TITLE = "Videopath Admin"

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "auth": {
        "user": ("email__icontains", "username__icontains",)
    },
    "users": {
        "team": ("owner__email__icontains", "owner__username__icontains", "name__icontains")
    }
}

#
#
#
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

#
# Change default user model
#
#AUTH_USER_MODEL = 'videopath.apps.users.model.user'

import django.conf.global_settings as DEFAULT_SETTINGS
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'raven.contrib.django.raven_compat', # error reporting with raven
    'django_extensions',
    #'south',
    'django_nose',
    'userena',
    'guardian',
    'easy_thumbnails',
    'rest_framework',
    'mathfilters',
    'videopath.apps.vp_admin',
    'videopath.apps.users',
    'videopath.apps.files',
    'videopath.apps.videos',
    'videopath.apps.analytics',
    'videopath.apps.payments',
    'videopath.apps.integrations'
)

#
# Userena Required Settings
#
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'videopath.backends.authentication.EmailAuthBackend'
)
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'users.UserSettings'
USERENA_SIGNIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/videopath/accounts/signin/'
LOGOUT_URL = '/videopath/accounts/signout/'

#
# django-rest-framework settings
#
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'videopath.apps.users.authentication.TokenAuthentication',
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/second',
    },
    'PAGE_SIZE': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100
}


#
# Required values for Heroku production environment
#
import logging
import sys

LOGGER = logging.getLogger('videopath')

# Log everything errors to console by default
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'videopath': {
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Required or get_host will fail on heroku
ALLOWED_HOSTS = ['*']

# Allow you to change the debug flag with an environment variable
if os.environ.get("DJANGO_DEBUG") == 'TRUE':
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG


# set default database to sqlite
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': 'test.db',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        'PORT': '',                      # Set to empty string for default.
    }
}
