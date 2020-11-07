from django.db import models

from videopath.apps.videos.models import Video, MarkerContent
from videopath.apps.common.models import VideopathBaseModel

#
# base model for all files
#
class VideopathFileBaseModel(VideopathBaseModel):
    key = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(32)
        super(VideopathFileBaseModel, self).save(*args, **kwargs)

#
# image file for marker content
#
class ImageFile(VideopathFileBaseModel):

    # status
    CREATED = 0
    FILE_RECEIVED = 1
    PROCESSING = 2
    PROCESSED = 3
    ERROR = -1
    STATUS_CHOICES = (
        (CREATED, 'Created. Waiting for upload.'),
        (FILE_RECEIVED, 'Uploaded.'),
        (PROCESSING, 'Processing'),
        (PROCESSED, 'Processed.'),
        (ERROR, 'Error.'),
    )

    # type
    MARKER_CONTENT = "marker content"
    CUSTOM_THUMBNAIL = "custom thumbnail"
    CUSTOM_LOGO = "custom logo"
    TYPE_CHOICES = (
        (MARKER_CONTENT, 'Image for Marker Content'),
        (CUSTOM_THUMBNAIL, 'Image for custom video thumbnail'),
        (CUSTOM_LOGO, 'Image for custom logo on player chrome'),
    )

    # marker content link
    markercontent = models.ManyToManyField(
        MarkerContent, related_name="image_file", blank=True)

    #
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CHOICES)
    image_type = models.CharField(
        max_length=255, blank=True, choices=TYPE_CHOICES, default=MARKER_CONTENT)

    # image data
    width = models.SmallIntegerField(default=0)
    height = models.SmallIntegerField(default=0)

    # file info
    bytes = models.BigIntegerField(default=0)
    original_file_name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s %s' % ("ImageFile", self.key)


