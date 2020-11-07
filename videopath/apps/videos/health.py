from django.conf import settings

from videopath.apps.common.services import service_provider


def check_access_to_player_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_PLAYER_BUCKET)

