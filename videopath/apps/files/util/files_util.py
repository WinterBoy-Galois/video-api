from django.conf import settings

from videopath.apps.files.models import ImageFile


def file_url_for_markercontent(content):
    try:
        file = content.image_file.latest("created")
        if file.status == ImageFile.PROCESSED:
            return settings.IMAGE_CDN + file.key
        return ""
    except:
        return ""