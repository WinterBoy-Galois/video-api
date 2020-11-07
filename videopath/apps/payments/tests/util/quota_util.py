from datetime import date

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.models import Video
from videopath.apps.analytics.models import DailyAnalyticsData
from videopath.apps.payments.util import quota_util
from videopath.apps.payments.models import QuotaInformation


class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()
        self.video = Video.objects.create(team=self.user.default_team)


    #
    # Check generation of the quota info table
    #
	def test_get_quota_info(self):

		# check if analytics data shows up in quota info
		DailyAnalyticsData.objects.create(
		    video=self.video, date=date.today(), plays_all=50)
		quota_info = quota_util.get_quota_info()
		self.assertEqual(quota_info[0]["views"], 50)


    #
    # Check that quota warning and exceeding is sent
    #
    def test_check_quotas(self):

        # simulate 1900 plays
        ad = DailyAnalyticsData.objects.create(video=self.video, date=date.today(), plays_all=9500000)
        quota_util.check_quotas()

        #assert that only the warning is true
        info = QuotaInformation.objects.get(user=self.user)
        self.assertTrue(info.warning_sent)
        self.assertFalse(info.quota_exceeded)

        # simulate 20mio plays
        ad.plays_all = 20000000
        ad.save()

        # see if handle user exceeded is called
        quota_util.check_quotas()

        # assert that both warning and exceed are now true
        info = QuotaInformation.objects.get(user=self.user)
        self.assertTrue(info.warning_sent)
        self.assertTrue(info.quota_exceeded)



