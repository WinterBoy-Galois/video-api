from django.test import TestCase

from videopath.apps.videos.models import Video
from videopath.apps.common.test_utils import create_simple_user

class ThumbnailsTest(TestCase):

    def setUp(self):
        self.user1 = create_simple_user()
        self.video = Video.objects.create(team=self.user1.default_team)
        self.video.save()


    # not working right now
    def test_manager(self):
        pass

