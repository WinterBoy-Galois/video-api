
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.common.services import service_provider

# Uses the standard django frame testing client
class TestClass(BaseTestCase):

    def setup(self):
        self.service = service_provider.get_service("video_source_import")
        self.assertIsNotNone(self.service)

    def test_youtube_import(self):
        source = self.service.import_video_from_url("https://www.youtube.com/watch?v=PPN3KTtrnZM")
        self.assertEqual(source["service"], "youtube")

    def test_vimeo_import(self):
        source = self.service.import_video_from_url("https://vimeo.com/36579366")
        self.assertEqual(source["service"], "vimeo")

    def test_wistia_import(self):
        source = self.service.import_video_from_url("http://fast.wistia.net/oembed?url=http://home.wistia.com/medias/1gaiqzxu03")
        self.assertEqual(source["service"], "wistia")

    def test_brightcove_import(self):
        source = self.service.import_video_from_url("http://players.brightcove.net/47628783001/default_default/index.html?videoId=3910607401001")
        self.assertEqual(source["service"], "brightcove")
        

    def test_server_import(self):
        source = self.service.import_video_from_server({
            "mp4":"http://videos.videopath.com/m35T1YU0KHQ8ZEr28fKgM4sS0zfEOQW3.mp4",
            "webm": "http://videos.videopath.com/m35T1YU0KHQ8ZEr28fKgM4sS0zfEOQW3.webm",
            "width":"320",
            "height":"240",
            "duration":"200"
          })
        self.assertEqual(source["service"], "custom")
       
       