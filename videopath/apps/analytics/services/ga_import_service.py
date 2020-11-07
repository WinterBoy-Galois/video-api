import json
import datetime
import time
import httplib2
import base64

from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

from django.db.models import Sum
from django.conf import settings

from videopath.apps.videos.models import Video, Marker
from videopath.apps.analytics.models import TotalAnalyticsData, DailyAnalyticsData
from videopath.apps.analytics.signals import analytics_imported

# const
view_id = "ga:83927052"
auth_scope = "https://www.googleapis.com/auth/analytics.readonly"

#
# Import data from google analytics
#
def import_data():

    service = _get_service()

    # import daily numbers yesterday
    datemapper = DateMapperDaily()
    datemapper.set_days_ago(1)
    for importer in importers:
        i = importer(datemapper, service)
        i.import_data()

    # import total numbers
    datemapper = DateMapperTotal()
    for importer in importers:
        i = importer(datemapper, service)
        i.import_data()

    # move total played numbers into video data
    for v in Video.objects.all():
        plays = DailyAnalyticsData.objects.filter(video=v).aggregate(Sum('plays_all'))
        plays = plays['plays_all__sum']
        if plays: v.total_plays = plays
        v.save()

    analytics_imported.send_robust(None)

    
#
# Import historical data from google analytics
#
def import_historical_data(offset=0):

    service = _get_service()

    c = offset
    while c < 5000:
      c = c + 1
      time.sleep(10)
      print str(c) + " ago"
      datemapper = DateMapperDaily()
      datemapper.set_days_ago(c)
      for importer in importers:
          i = importer(datemapper,service)
          i.import_data()


#
# get the service object
#
def _get_service():
    key = base64.standard_b64decode(settings.GA_PRIVATE_KEY)
    credentials = SignedJwtAssertionCredentials(settings.GA_EMAIL, key, auth_scope)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v3', http=http)
    return service


# map date to database rows

class DateMapper:

    def __init__(self):
        self.row_cache = {}

    def get_range(self):
        return None, None

    def get_database_row(self, id):
        if id in self.row_cache:
            return self.row_cache[id]
        row = self.get_database_row_uncached(id)
        self.row_cache[id] = row
        return row

    def get_database_row_uncached(self, id):
        return None


class DateMapperTotal(DateMapper):

    def get_range(self):
        return "2006-01-01", "2020-01-01"

    def get_database_row_uncached(self, id):
        try:
            #if id != "1PgRRon5":
            #    return None
            v = Video.objects.get(key=id)
            row, created = TotalAnalyticsData.objects.get_or_create(video=v)
            return row
        except Video.DoesNotExist:
            return None


class DateMapperDaily(DateMapper):

    def __init__(self):
        self.set_days_ago(1)

    def set_days_ago(self, days_ago):
        self.row_cache = {}
        self.date = datetime.date.today() - datetime.timedelta(days=days_ago)

    def get_range(self):
        datestring = "{:%Y-%m-%d}".format(self.date)
        return datestring, datestring

    def get_database_row_uncached(self, id):
        try:
            v = Video.objects.get(key=id)
            row, created = DailyAnalyticsData.objects.get_or_create(
                video=v, date=self.date)
            return row
        except Video.DoesNotExist:
            return None


# get google analytics feed

class MetricsImport:

    def __init__(self, datemapper, service):
        self.service = service
        self.max_results = 10000
        self.current_offset = 1
        self.datemapper = datemapper

    def get_query_args(self):
        return {}

    def get_entries(self):
        start_date, end_date = self.datemapper.get_range()
        query_args = self.get_query_args()
        default_args = {
            'ids': view_id,
            'dimensions': 'ga:dimension1',
            'metrics': 'ga:visits',
            'sort': 'ga:dimension1',
            'start_date': start_date,
            'end_date': end_date,
            'max_results': self.max_results,
            'start_index': self.current_offset
        }

        # contruct query args and get results
        query_args = dict(default_args.items() + query_args.items())
        results = self.service.data().ga().get(**query_args).execute()

        self.current_offset += self.max_results
        return results.get("rows"), results.get("totalResults") > self.current_offset

    def process_start(self):
        pass

    def process_row(self, entry, row, video_key):
        pass

    def process_end(self):
        pass

    def import_data(self):
        has_more = True

        self.process_start()
        while has_more:
            entries, has_more = self.get_entries()
            if not entries:
                continue
            for entry in entries:
                video_key = entry.pop(0)
                row = self.datemapper.get_database_row(video_key)
                if row:
                    self.process_row(entry, row, video_key)
                    row.save()
        self.process_end()


# import plays
class MetricsImportPlays(MetricsImport):

    def get_query_args(self):
        return {
            'metrics': 'ga:uniqueEvents, ga:newUsers',
            'filters': 'ga:eventAction==play'
        }

    def process_row(self, entry, row,video_key):
        plays_by_all_users = entry[0]
        plays_by_new_users = entry[1]

        row.plays_all = plays_by_all_users
        row.plays_unique = plays_by_new_users


# import markers clicked
class MetricsImportMarkersClicked(MetricsImport):

    def get_query_args(self):
        return {
            'metrics': 'ga:totalEvents, ga:uniqueEvents',
            'filters': 'ga:eventAction==show overlay'
        }

    def process_row(self, entry, row, video_key):
        row.overlays_opened_all = entry[0]
        row.overlays_opened_unique = entry[1]


# import session duration
class MetricsImportSessionDuration(MetricsImport):

    def get_query_args(self):
        return {
            'metrics': 'ga:avgSessionDuration',
        }

    def process_row(self, entry, row, video_key):
        row.avg_session_time = entry[0]

# import video completed


class MetricsImportVideoCompleted(MetricsImport):

    def get_query_args(self):
        return {
            'metrics': 'ga:uniqueEvents',
            'filters': 'ga:eventAction==video ended'
        }

    def process_row(self, entry, row, video_key):
        row.video_completed = entry[0]

# import video sessions


class MetricsImportSessions(MetricsImport):

    def get_query_args(self):
        return {
            'metrics': 'ga:uniqueEvents',
            'filters': 'ga:eventAction==pathplayer ready'
        }

    def process_row(self, entry, row, video_key):
        row.sessions = entry[0]

# import list of popular markers
class MetricsPopularMarkers(MetricsImport):

    def get_query_args(self):
        return {
            'dimensions': 'ga:dimension1, ga:eventLabel',
            'metrics': 'ga:totalEvents, ga:uniqueEvents',
            'filters': 'ga:eventAction==show overlay'
        }

    def process_start(self):
        self.video_cache = {}

    def process_end(self):
        self.video_cache = {}

    def process_row(self, entry, row, video_key):

        # try to load marker name
        marker_key = entry.pop(0)

        marker_name = "Deleted"
        marker = None
        try:
            marker = Marker.objects.filter(key__iexact=marker_key).latest('modified')
        except Marker.DoesNotExist:
            try:
                marker = Marker.objects.filter(id=int(marker_key)).latest('modified')
            except Marker.DoesNotExist:
                pass
            except ValueError:
                pass

        # if there is no marker, or it is associated with the wrong video
        # return
        if not marker or marker.video_revision.video.key != video_key:
            return

        marker_id = marker.key
        marker_name = marker.title

        marker_info = {
            "total": int(entry[0]),
            "unique": int(entry[1]),
            "name": marker_name
        }

        # create entry in video cache if needed
        marker_cache = {}
        if video_key in self.video_cache:
            marker_cache = self.video_cache[video_key]
        else:
            self.video_cache[video_key] = marker_cache
        

        # if we have something in the cache, add it
        if marker_id in marker_cache:
            marker_info["total"] += marker_cache[marker_id]["total"]
            marker_info["unique"] += marker_cache[marker_id]["unique"]

        marker_cache[marker_id] = marker_info
        row.popular_markers = json.dumps(marker_cache)

#
# used by health checks to check access
#
def check_access():
    try:
        _get_service()
        return True
    except Exception as e:
        return str(e)


#
# Define which importers to use
#
importers = [
    MetricsImportPlays,
    MetricsImportMarkersClicked,
    MetricsImportSessionDuration,
    MetricsPopularMarkers,
    MetricsImportVideoCompleted,
    MetricsImportSessions
]

