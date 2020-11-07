from django.conf import settings

from videopath.apps.common.services import service_provider


def check_access_to_video_in_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_UPLOAD_BUCKET)

def check_access_to_logs_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_LOGS_BUCKET)

def check_access_to_videos_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_VIDEOS_BUCKET)

def check_access_to_thumbnail_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_THUMBNAIL_BUCKET)

# def check_access_to_video_backup_bucket():
# 	service = service_provider.get_service("s3")
# 	return service.check_access_to_bucket(settings.AWS_VIDEO_BACKUP_BUCKET)

def check_access_to_image_out_bucket():
	service = service_provider.get_service("s3")
	return service.check_access_to_bucket(settings.AWS_IMAGE_OUT_BUCKET)