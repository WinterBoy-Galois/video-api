import json

from rest_framework import serializers

from videopath.apps.analytics.models import TotalAnalyticsData, DailyAnalyticsData, VideoStatistics

#
# Basic analytics 
#
class BaseAnalyticsDataSerializer(serializers.ModelSerializer):
    percent_interacting = serializers.SerializerMethodField()
    percent_completing = serializers.SerializerMethodField()
    clicks_per_user = serializers.SerializerMethodField()
    popular_markers = serializers.SerializerMethodField()

    def get_percent_interacting(self, data):
        if data.plays_all <= 0:
            return 0
        return min(100, (float(data.overlays_opened_unique / float(data.plays_all)) * 100))

    def get_clicks_per_user(self, data):
        if data.plays_all <= 0:
            return 0
        return (float(data.overlays_opened_all) / float(data.plays_all))

    def get_percent_completing(self, data):
        if data.plays_all <= 0:
            return 0
        return min(100, (float(data.video_completed / float(data.plays_all)) * 100))

    def get_popular_markers(self, data):
        return json.loads(data.popular_markers)
#
# Base serialzer fields
#
base_fields = ('video', 'video_completed', 'plays_all', 'plays_unique', 'avg_session_time', 'overlays_opened_unique',
              'overlays_opened_all', 'percent_interacting', 'clicks_per_user', 'popular_markers', 'percent_completing')


#
# Overall data
#
class TotalAnalyticsDataSerializer(BaseAnalyticsDataSerializer):
    class Meta:
        fields = base_fields
        model = TotalAnalyticsData

#
# Daily Data
#
class DailyAnalyticsDataSerializer(BaseAnalyticsDataSerializer):
    class Meta:
        fields = base_fields + ('date',)
        model = DailyAnalyticsData
