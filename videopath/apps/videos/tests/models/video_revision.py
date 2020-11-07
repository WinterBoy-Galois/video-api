
from videopath.apps.videos.models import Video, MarkerContent, Marker
from videopath.apps.common.test_utils import BaseTestCase

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
        video = Video.objects.create(team=self.user.default_team)
        self.assertIsNotNone(video.draft)

    def test_duplication(self):
        video = Video.objects.create(team=self.user.default_team)

    	markers =[
    		Marker.objects.create(video_revision=video.draft),
    		Marker.objects.create(video_revision=video.draft),
    	]

    	MarkerContent.objects.create(marker=markers[0])
    	MarkerContent.objects.create(marker=markers[0])
    	MarkerContent.objects.create(marker=markers[0])
    	MarkerContent.objects.create(marker=markers[1])

    	video.draft.duplicate()

    	self.assertEqual(Marker.objects.count(), 4)
    	self.assertEqual(MarkerContent.objects.count(), 8)


    def test_password(self):
        video = Video.objects.create(team=self.user.default_team)
        revision = video.draft

        # test if settings password adds hash and salted version of pw
        revision.password = "super secret"
        revision.save()
        self.assertIsNotNone(revision.password_hashed)
        self.assertIsNotNone(revision.password_salt)



