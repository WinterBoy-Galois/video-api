from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.common import test_utils
from videopath.apps.videos.models import Video, Marker, VideoRevision, MarkerContent

# Uses the standard django frame testing client
class EndpointsBaseTestCase(BaseTestCase):

    def setup(self):
        # do some setup stuff
        pass

    def test_something(self):
        # do some testing
        pass
