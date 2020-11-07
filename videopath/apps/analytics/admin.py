from django.contrib import admin

from videopath.apps.analytics.models import TotalAnalyticsData, DailyAnalyticsData, VideoStatistics

class TotalAnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('video', 'plays_all', 'plays_unique',
                    'overlays_opened_all', 'avg_session_time', 'video_completed', 'sessions')
    search_fields = ['video__id']

    raw_id_fields = ['video',]
    autocomplete_lookup_fields = {
        'fk': ['video',],
    }

class DailyAnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('video', 'date', 'plays_all', 'plays_unique',
                    'overlays_opened_all', 'avg_session_time', 'video_completed', 'sessions')
    ordering = ('-date',)
    search_fields = ['video__id']
    
    raw_id_fields = ['video',]
    autocomplete_lookup_fields = {
        'fk': ['video',],
    }

class VideoStatisticsAdmin(admin.ModelAdmin):
    list_display = ('created', 'sessionTotal', 'playingTotal', 'overlayOpenTotal', 'progressMax', 'videoKey', 'video_link')
    ordering = ('-created',)

    search_fields = ['videoKey']

    def video_link(self, obj):
        link = "/admin/insights/videos/" + str(obj.videoKey) + "/"
        return "<a href = '" + link + "'>Link</a>"
    video_link.allow_tags = True



admin.site.register(TotalAnalyticsData, TotalAnalyticsDataAdmin)
admin.site.register(DailyAnalyticsData, DailyAnalyticsDataAdmin)
admin.site.register(VideoStatistics, VideoStatisticsAdmin)
