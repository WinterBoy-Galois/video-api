from django.core.cache import cache
from django.db import connection

from videopath.apps.common.services import service_provider

#
# External services
#
def check_stripe_access():
	service = service_provider.get_service("stripe")
	return service.check_access()

def check_transcoder_access():
	service = service_provider.get_service("elastic_transcoder")
	return service.check_connection()

def check_s3_access():
	service = service_provider.get_service("s3")
	return service.check_access()

def check_cloundfront_access():
	service = service_provider.get_service("cloudfront")
	return service.check_access()

def check_mandrill_access():
	service = service_provider.get_service("mail")
	return service.check_access()

def check_mailchimp_access():
	service = service_provider.get_service("mailchimp")
	return service.check_access()

def check_raven_sentry_connection():
	from raven.scripts.runner import send_test_message
	from raven.contrib.django.models import client
	try:
		send_test_message(client, {})
		return True
	except:
		return "could not connect to sentry"

def check_geo_ip():
	service = service_provider.get_service("geo_ip")
	record = service.record_by_address("84.159.212.138")
	if record["country"] == "DE" and record["continent"] == "EU":
		return True
	else:
		return "Lookup failed"

def check_video_import_youtube():
	service = service_provider.get_service("video_source_import")
	try:
		source = service.import_video_from_url("https://www.youtube.com/watch?v=2rtGFAnyf-s")
		return source["service"] == "youtube"
	except Exception as e:
		return e.message

def check_video_import_vimeo():
	service = service_provider.get_service("video_source_import")
	try:
		source = service.import_video_from_url("https://vimeo.com/36579366")
		return source["service"] == "vimeo"
	except:
		return "Vimeo import failed"
		
def check_video_import_wistia():
	service = service_provider.get_service("video_source_import")
	try:
		source = service.import_video_from_url("http://fast.wistia.net/oembed?url=http://home.wistia.com/medias/1gaiqzxu03")
		return source["service"] == "wistia"
	except:
		return "Wistia import failed"

def check_import_brightcove():
	return True
	service = service_provider.get_service("video_source_import")
	try:
		source = service.import_video_from_url("http://players.brightcove.net/47628783001/default_default/index.html?videoId=3910607401001")
		return source["service"] == "brightcove"
	except:
		return "Brightcove import failed"
	
#TODO: replace with celery
#def check_services_connection():
#	service = service_provider.get_service("services")
#	return service.test_connection()

#
# Django stuff
#

# database
def check_db_connection():
	try:
		cursor = connection.cursor()
		cursor.execute("select 1")
		return True
	except Exception as e:
		return str(e)

# cache
def check_cache():
	cache.set('cache_test', 'itworks', 1)
	if cache.get("cache_test") == "itworks":
		return True
	else:
		return 	"Caching appears to be offline"
