from django.conf import settings

from rest_framework import serializers

from videopath.apps.files.models import  ImageFile
from videopath.apps.files.settings import image_sizes


#
#
#
class ImageFileSerializer(serializers.ModelSerializer):

    representations = serializers.SerializerMethodField()

    def get_representations(self, imagefile):
        conf = image_sizes[imagefile.image_type]
        result = {}
        for out in conf["outs"]:
            result[out["name"]] = settings.IMAGE_CDN + \
                out["key"].replace("_FILEKEY_", imagefile.key)
        return result

    class Meta:
        model = ImageFile
        fields = ('status', 'representations')
