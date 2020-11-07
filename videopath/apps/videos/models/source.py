from django.db import models
from django.db.models import Q

from videopath.apps.common.models import VideopathBaseModel

from django.conf import settings

from videopath.apps.common.services import service_provider

#
# Layout new source class
# not in use at the moment
#
class Source(VideopathBaseModel):

    # status
    STATUS_WAITING = "awaiting_upload"
    STATUS_PROCESSING = "processing"
    STATUS_OK = "ok"
    STATUS_ERROR = "error"

    STATUS_CHOICES = (
        (STATUS_WAITING, STATUS_WAITING),
        (STATUS_PROCESSING, STATUS_PROCESSING),
        (STATUS_OK, STATUS_OK),
        (STATUS_ERROR, STATUS_ERROR),
    )

    # service
    SERVICE_NONE = "none"
    SERVICE_VIDEOPATH = "videopath"
    SERVICE_YOUTUBE = "youtube"
    SERVICE_VIMEO = "vimeo"
    SERVICE_WISTIA = "wistia"
    SERVICE_BRIGHTCOVE = "brightcove"
    SERVICE_VIDEOPATH = "videopath"
    SERVICE_CUSTOM = "custom"
    SERVICE_MOVINGIMAGES = "movingimages"
    SERVICE_CHOICES = (
        (SERVICE_NONE, SERVICE_NONE),
        (SERVICE_YOUTUBE, SERVICE_YOUTUBE),
        (SERVICE_VIMEO, SERVICE_VIMEO),
        (SERVICE_WISTIA, SERVICE_WISTIA),
        (SERVICE_BRIGHTCOVE, SERVICE_BRIGHTCOVE),
        (SERVICE_VIDEOPATH, SERVICE_VIDEOPATH),
        (SERVICE_CUSTOM, SERVICE_CUSTOM),
        (SERVICE_MOVINGIMAGES,SERVICE_MOVINGIMAGES)
    )

    # unique id
    key = models.CharField(max_length=50, blank=True, unique=True)

    # status settings
    status = models.CharField(max_length=255, default=STATUS_OK, choices=STATUS_CHOICES)

    # service & id, such as youtube or vimeo id
    service_identifier = models.CharField(max_length=255, default="")
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES, default=SERVICE_NONE)

    # media data
    duration = models.FloatField(default=0)
    aspect = models.FloatField(default=0)
    description = models.CharField(max_length=255, default="")

    # images  
    thumbnail_small = models.CharField(max_length=2048, default="")
    thumbnail_large = models.CharField(max_length=2048, default="")

    # source files (for videopath and own hosting)
    file_mp4 = models.CharField(max_length=512, default="", blank=True)
    file_webm = models.CharField(max_length=512, default="", blank=True)

    # yt special setting
    youtube_allow_clickthrough = models.BooleanField(default=False)

    # videopath
    notes = models.CharField(max_length=255, blank=True)

    sprite_support = models.BooleanField(default=False)
    sprite_length = models.IntegerField(default=0)

    #
    # get a list of all video objects associated with this source
    #
    def get_attached_videos(self):
        from videopath.apps.videos.models import Video
        return Video.objects.filter( Q(draft__source__key = self.key) | Q(current_revision__source__key = self.key))


    #
    # send a message to services that we want to transcode jpgs for this source
    #
    def export_jpg_sequence(self):

        if self.sprite_support:
            return  False, "Project is already transcoded for iPhone."
        if self.duration > 660:
            return False, "Currently only projects shorter than 10 Minutes can be transcoded."
        if self.service not in [Source.SERVICE_YOUTUBE, Source.SERVICE_VIMEO, Source.SERVICE_VIDEOPATH, Source.SERVICE_CUSTOM]:
            return False, "Currently only youtube and vimeo projects can be transcoded."

        service_connection = service_provider.get_service('services')
        service_connection.send_message('x-transcoder', {'source': 
                {
                'key':self.key,
                'service': self.service,
                'service_identifier': self.service_identifier,
                'file_mp4': self.file_mp4
                }
            })

        return True, 'Video sent to be exported'

    #
    # get correct tumbnails for this source object
    #
    def get_thumbnails(self):
        if self.service == 'videopath':
            return {
                "normal": settings.THUMBNAIL_CDN + self.thumbnail_small,
                "large": settings.THUMBNAIL_CDN + self.thumbnail_large
            }
        else:
            return {
                "normal": self.thumbnail_small,
                "large": self.thumbnail_large
            } 

    #
    #
    #
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(32)
        super(Source, self).save(*args, **kwargs)