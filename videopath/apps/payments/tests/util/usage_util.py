from datetime import date

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.models import Video
from videopath.apps.payments.util import usage_util
from videopath.apps.analytics.models import DailyAnalyticsData

class TestCase(BaseTestCase):

	def setup(self):
		self.create_user()
		self.video = Video.objects.create(team=self.user.default_team)


	def test_usage_current(self):
		DailyAnalyticsData.objects.create(video=self.video, date=date.today(), plays_all=200)
		DailyAnalyticsData.objects.create(video=self.video, date=date.today(), plays_all=400)
		DailyAnalyticsData.objects.create(video=self.video, date=date.today(), plays_all=600)
		
		result = usage_util.plan_usage_current(self.user);
		self.assertEqual(result, 1200)




