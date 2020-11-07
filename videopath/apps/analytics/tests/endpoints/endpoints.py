from videopath.apps.common.test_utils import BaseTestCase
import datetime

from videopath.apps.videos.models import Video
from videopath.apps.analytics.models import DailyAnalyticsData, TotalAnalyticsData

DAILY_URL = "/v1/video/{0}/analytics-daily/?start=0&end=4075742868"
TOTAL_URL = "/v1/video/{0}/analytics/"

# Uses the standard django frame testing client
class EndpointsBaseTestCase(BaseTestCase):
        
    def setup(self):
        self.setup_users_and_clients()

        self.video = Video.objects.create(team=self.user1.default_team)

        DailyAnalyticsData.objects.create(video=self.video, date=datetime.date.today())
        TotalAnalyticsData.objects.create(video=self.video)

    def test_endpoints(self):


        response = self.client_user1.get_json(TOTAL_URL.format(self.video.id))
        self.assertEqual(response.data.get("count"), 1);
        self.assertEqual(response.status_code, 200)

        response = self.client_user1.get_json(DAILY_URL.format(self.video.id))
        self.assertEqual(response.data.get("count"), 1);
        self.assertEqual(response.status_code, 200)


        ## user 2 should have no access
        response = self.client_user2.get_json(TOTAL_URL.format(self.video.id))
        self.assertEqual(response.data.get("count"), 0);
        self.assertEqual(response.status_code, 200)

        response = self.client_user2.get_json(DAILY_URL.format(self.video.id))
        self.assertEqual(response.data.get("count"), 0);
        self.assertEqual(response.status_code, 200)

