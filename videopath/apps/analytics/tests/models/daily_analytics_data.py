import datetime

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.models import Video
from videopath.apps.analytics.models import DailyAnalyticsData

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	video = Video.objects.create(team=self.user.default_team)
    	data = DailyAnalyticsData.objects.create(video=video, date=datetime.date.today())
        self.assertIsNotNone(data)