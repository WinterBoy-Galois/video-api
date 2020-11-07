import copy

from django.db import models

from videopath.apps.common.models import VideopathBaseModel
from videopath.apps.videos.models.video_revision import VideoRevision


class Markers(models.Manager):

    def filter_for_user(self,user):
        return self.filter( models.Q(video_revision__video__team__owner = user) | models.Q(video_revision__video__team__members = user) )

class Marker(VideopathBaseModel):

    objects = Markers()

    # key
    key = models.CharField(max_length=50, blank=True, db_index=True)

    # base stuff
    video_revision = models.ForeignKey(VideoRevision, related_name="markers")
    title = models.CharField(max_length=100, blank=True)
    time = models.FloatField(default=0, null=False, blank=False)

    def has_user_access(self, user, readonly=True):
        return self.video_revision.has_user_access(user, readonly)

    # duplicate the marker
    def duplicate(self):
        duplicate = copy.copy(self)
        duplicate.pk = None
        duplicate.save()

        for content in self.contents.all():
            dup_content = content.duplicate()
            dup_content.marker = duplicate
            dup_content.save()

        return duplicate

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(8)
        super(Marker, self).save(*args, **kwargs)

    class Meta:
        app_label = "videos"

