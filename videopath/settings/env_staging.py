
#
# Set staging var to true
#
STAGING = True

#
# Set Heroku DB
#
import dj_database_url
if dj_database_url.config():
    DATABASES['default'] = dj_database_url.config()

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#
# Set dev player locations
#
AWS_PLAYER_BUCKET = "player-dev.videopath.com"
PLAYER_SRC = '//player-dev.videopath.com/develop/'
PLAYER_LOCATION = 'http://player-dev.videopath.com/'

IMAGE_CDN = 'https://vp-images-dev.s3-us-west-1.amazonaws.com/'
AWS_IMAGE_OUT_BUCKET = "vp-images-dev"

#
# Endpoint for JPG engine streaming
#
JPGS_CDN = '//videopathmobilefilesdev.blob.core.windows.net/'

#
# Integrations
#

#
# Endpoint
#
API_ENDPOINT = 'https://api-dev.herokuapp.com'

APP_URL = 'https://app-dev.videopath.com/develop'
