import re

from datetime import date 

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view

from videopath.apps.analytics.models import TotalAnalyticsData, DailyAnalyticsData, VideoStatistics
from videopath.apps.analytics.serializers import TotalAnalyticsDataSerializer, DailyAnalyticsDataSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 365
    page_size_query_param = 'page_size'
    max_page_size = 365

class TotalAnalyticsDataViewSet(viewsets.ReadOnlyModelViewSet):

    model = TotalAnalyticsData
    serializer_class = TotalAnalyticsDataSerializer

    # Can see only your videos
    def get_queryset(self, vid = None, *args, **kwargs):
        # for some reason, vid does not get forwarded
        # hack to fix this here....
        r = re.compile('video/(.*?)/ana')
        m = r.search(self.request.path)
        vid = m.group(1)
        return TotalAnalyticsData.objects.filter_for_user(self.request.user).filter(video__id=vid).distinct()

class DailyAnalyticsDataViewSet(viewsets.ReadOnlyModelViewSet):

    model = DailyAnalyticsData
    serializer_class = DailyAnalyticsDataSerializer
    pagination_class = LargeResultsSetPagination

    # Can see only your videos
    def get_queryset(self, vid=None):
        # for some reason, vid does not get forwarded
        # hack to fix this here....
        r = re.compile('video/(.*?)/ana')
        m = r.search(self.request.path)
        vid = m.group(1)
        start = date.fromtimestamp(int(self.request.GET.get("start", 0)))
        end = date.fromtimestamp(int(self.request.GET.get("end", 0)))
        return DailyAnalyticsData.objects.filter_for_user(self.request.user).filter(video__id=vid, date__range=[start, end]).distinct().order_by('date')

#
# "Login" and "Logout" methods
#
@api_view(['POST'])
@permission_classes((AllowAny,))
def stats(request):
    
    try:
        values = {
            'playingTotal': float(request.data.get('playingTotal', 0)),
            'overlayOpenTotal': float(request.data.get('overlayOpenTotal', 0)),
            'progressMax': float(request.data.get('progressMax', 0)),
            'sessionTotal': float(request.data.get('sessionTotal', 0)),
            'videoKey': request.data.get('videoKey', None)
        }

        sessionKey = request.data.get('sessionKey', None)
        
        if sessionKey is not None and values['playingTotal'] > 0 and values['sessionTotal'] > 0:
            VideoStatistics.objects.update_or_create(sessionKey=sessionKey, defaults=values)
            
    except:
        pass

    return Response()