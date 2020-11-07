from datetime import date, timedelta

from django.conf import settings

from videopath.apps.common.services import service_provider


def check_access_to_dumps_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_DB_DUMPS_BUCKET)

#
# Check that db backups are being made
#
# disabled for now
def c_heck_most_recent_backup():


	service = service_provider.get_service("s3")
	yesterday = date.today()  - timedelta(1)
	prefix = "videopath-api/" + yesterday.strftime("%Y-%m-%d")
	length = len(list(service.list_keys(settings.AWS_DB_DUMPS_BUCKET, prefix)))

	if length > 0:
		return True
	else:
		return "There does not appear to be a recent backup of the database."