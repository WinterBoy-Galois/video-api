from videopath.apps.common.services.cloudfront_custom.CloudFrontConnection import CloudFrontConnection
from django.conf import settings

if not settings.LOCAL:
	connection = CloudFrontConnection()

def invalidate(distribution_id, path):
	if not settings.LOCAL:
		connection.create_invalidation_request(distribution_id, path)
	return True

def check_access():
	try:
		connection.get_all_distributions()
		return True
	except:
		return "Could not connect to Cloudfront"