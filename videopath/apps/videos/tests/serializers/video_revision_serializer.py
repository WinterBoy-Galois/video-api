
from videopath.apps.videos.models import Video
from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.videos.serializers import VideoRevisionSerializer, VideoRevisionDetailSerializer

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
        pass

    def test_publish_unpublish(self):
      	pass