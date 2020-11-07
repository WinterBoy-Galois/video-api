from django.db import models

from videopath.apps.common.models import VideopathBaseModel

class BaseAnalyticsData(VideopathBaseModel):

    # stats
    sessions = models.IntegerField(default=0)
    plays_all = models.IntegerField(default=0)
    plays_unique = models.IntegerField(default=0)
    overlays_opened_all = models.IntegerField(default=0)
    overlays_opened_unique = models.IntegerField(default=0)
    avg_session_time = models.FloatField(default=0)
    popular_markers = models.TextField(default="{}")
    video_completed = models.IntegerField(default=0)

    class Meta:
        abstract = True