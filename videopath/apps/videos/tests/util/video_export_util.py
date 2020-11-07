
from videopath.apps.videos.models import Video
from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.videos.util import video_export_util

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

	def setup(self):
	    self.create_user()

	def test_export_video(self):
	    
		# video should be creatable 
		video = Video.objects.create(team=self.user.default_team)
			
		video_export_util.export_video(video)
		self.assertEqual(True, True)
		
	def test_export_util_password(self):
		video = Video.objects.create(team=self.user.default_team)
		video.draft.password = "super secret"
		video.draft.save()
		video_export_util.export_video(video)
		self.assertEqual(True, True)

