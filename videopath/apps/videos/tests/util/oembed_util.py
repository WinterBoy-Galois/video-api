
from videopath.apps.videos.models import Video, VideoRevision
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.util import  oembed_util

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.setup_users()
        self.video = Video.objects.create(team=self.user.default_team)

    def test_invalid_urls(self):

        result = oembed_util.parse({'url':'http://google.de'})
        self.assertEqual(result, 404)

        result = oembed_util.parse({'url':'http://videopath.com/9823049'})
        self.assertEqual(result, 404)

        result = oembed_util.parse({'url':'http://player.videopath.com//'})
        self.assertEqual(result, 404)

    def test_valid_url_but_unpublished_video(self):
        result = oembed_util.parse({'url':'http://player.videopath.com/' + self.video.key})
        self.assertEqual(result, 401)


    def test_valid_video(self):

      revision = VideoRevision.objects.create(video=self.video)
      self.video.current_revision = revision
      self.video.published = 1
      self.video.save()

      result = oembed_util.parse({'url':'http://player.videopath.com/' + self.video.key})
      self.assertEqual(result['provider_name'], 'Videopath')
      self.assertEqual(result['provider_media_id'],  self.video.key)
