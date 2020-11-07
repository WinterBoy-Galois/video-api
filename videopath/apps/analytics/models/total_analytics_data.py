from django.db import models

from videopath.apps.analytics.models.base_analytics_data import BaseAnalyticsData
from videopath.apps.videos.models import Video

class TotalAnalyticsDatas(models.Manager):

    def filter_for_user(self,user):
        return self.filter( models.Q(video__team__owner = user) | models.Q(video__team__members = user) )


class TotalAnalyticsData(BaseAnalyticsData):

	objects = TotalAnalyticsDatas()

	video = models.ForeignKey(Video, related_name="total_analytics")

	class Meta:
	    app_label = "analytics"