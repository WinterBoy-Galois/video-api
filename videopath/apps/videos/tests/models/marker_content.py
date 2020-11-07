
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.models import Video, Marker, MarkerContent

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
        video = Video.objects.create(team=self.user.default_team)
        marker = Marker.objects.create(video_revision = video.draft)
        marker_content = MarkerContent(marker=marker)
       	self.assertIsNotNone(marker_content)
