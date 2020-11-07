from videopath.apps.common.util import image_resize_util
import string, random

from django.conf import settings

from videopath.apps.common.services import service_provider

def handle_uploaded_icon(video_revision,f):

	if not f:
		return False, "No File"

	try:
		fname = image_resize_util.resize_image_file(f, {
			"operation":"fit",
			"size":(52,52)
			})
	except:
		return False, "Could not interpret your file. Are you sure you uploaded an image?"

	s3_service = service_provider.get_service("s3")
	key = _random_string()
	video_revision.ui_icon = key
	video_revision.save()
	s3_service.upload(fname, settings.AWS_IMAGE_OUT_BUCKET, '/' + settings.AWS_IMAGE_ICON_FOLDER + '/' + key, public=True)

	return True, None

def _random_string():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))