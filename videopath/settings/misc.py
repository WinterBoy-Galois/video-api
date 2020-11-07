import os

#
# define wether mock versions of services should be loaded
#
SERVICE_MOCKS = False

#
# Setup mem cachify caches
#
from memcacheify import memcacheify
CACHES = memcacheify()

#
# Player config for export
#
PLAYER_DEFAULT_VERSION = '6'
PLAYER_SRC = '//src.videopath.com/player/'
PLAYER_LOCATION = 'http://player.videopath.com/'

#
# CDN Endpoints
#
VIDEO_CDN = '//videos.videopath.com/'
THUMBNAIL_CDN = '//thumbs.videopath.com/'
IMAGE_CDN = 'https://images.videopath.com/'
DOCS_CDN = "https://docs.videopath.com/"

#
# demo videos
#
DEMO_VIDEOS = {
    "1": "2rtGFAnyf-s"
}

#
# Maintenance mode
#
MAINTENANCE_IP = os.environ.get("MAINTENANCE_IP", None)

#
# Invoice Numbers
#
INVOICE_START_NUMBER = 32049

#
# URL for pg backups on heroku
#
PGBACKUPS_URL = os.environ.get("PGBACKUPS_URL")

#
# Endpoint for JPG engine streaming
#
JPGS_CDN = '//az744831.vo.msecnd.net/'

#
# Default values for appearance
#
DEFAULT_VIDEO_APPEARANCE = {

	# Language of the interface, notably the "click me" alert.
    "ui_language": "en", 

    # custom colors
    "ui_color_1": None, 
    "ui_color_2": None, 

    # logos & icons
    "endscreen_logo": None, 
    "ui_icon": None,
    # "ui_icon_link_target": "https://videopath.com",

    #
    "ui_click_hint_color": "#ffffff",
    "ui_click_hint_appearences": 1

}

#
# Available currencies
#
CURRENCY_USD = "USD"
CURRENCY_EUR = "EUR"
CURRENCY_GBP = "GBP"

CURRENCY_SETTINGS = {
    CURRENCY_USD: {
        'plan_string': 'price_usd',
        'symbol': '$',
        'name': 'US Dollars'
    },
    CURRENCY_GBP: {
        'plan_string': 'price_gbp',
        'symbol': '&pound;',
        'name': 'British Pounds'
    },
    CURRENCY_EUR: {
        'plan_string': 'price_eur',
        'symbol': '&euro;',
        'name': 'Euro'
    }
}
CURRENCY_CHOICES = [(k, v["name"]) for k, v in CURRENCY_SETTINGS.iteritems()]

#
# Available payment providers
#
PAYMENT_PROVIDER_OTHER = "other"
PAYMENT_PROVIDER_STRIPE = "stripe"
PAYMENT_PROVIDER_TRANSFER = "transfer"
PAYMENT_PROVIDER_CHOICES = (
    (PAYMENT_PROVIDER_OTHER, PAYMENT_PROVIDER_OTHER),
    (PAYMENT_PROVIDER_STRIPE, PAYMENT_PROVIDER_STRIPE),
    (PAYMENT_PROVIDER_TRANSFER, PAYMENT_PROVIDER_TRANSFER)
)

#
# Rabbit MQ Connection
#
CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL', '')

#
# Own URL
#
API_ENDPOINT = 'https://api.videopath.com'

#
# App address
#
APP_URL = 'https://app.videopath.com'


