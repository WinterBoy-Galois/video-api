from django.test import TestCase
from django.conf import settings

from videopath.apps.common.services import service_provider

# Uses the standard django frame testing client
class TestClass(TestCase):

    def setUp(self):
        # do some setup stuff
        self.service = service_provider.get_service("elastic_transcoder")
        self.assertIsNotNone(self.service)

    def test_start_job(self):
		# do some testing

		t_input = {
		    'Key': "some key",
		}

		t_output_mp4 = {
		    'Key': "some key.mp4",
		    'ThumbnailPattern': 'some key' + '/{count}-hd',
		    'Rotate': 'auto',
		    'PresetId': settings.AWS_TRANSCODE_PRESET_ID
		}

		self.service.start_transcoding_job(t_input, None, [t_output_mp4])
