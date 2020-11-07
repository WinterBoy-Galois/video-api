from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.videos.models import Video, Marker, MarkerContent
from videopath.apps.files.models import ImageFile

REQUEST_URL = '/v1/image/upload/requestticket/{0}/{1}/'
COMPLETE_URL = '/v1/image/upload/complete/{0}/'

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def test_upload_thumbnail(self):
		self.setup_users_and_clients()
		v=Video.objects.create(team=self.user.default_team)

		# test creation of ticket
		response = self.client_user1.get(REQUEST_URL.format("custom_thumbnail", v.draft.pk))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(ImageFile.objects.count(), 1)
		ticket_id = response.data["ticket_id"]

		# test complete notification
		response = self.client_user1.get(COMPLETE_URL.format(ticket_id))
		self.assertEqual(response.status_code, 200)


    def test_upload_marker_content_image(self):
		self.setup_users_and_clients()
		v=Video.objects.create(team=self.user.default_team)
		m=Marker.objects.create(video_revision=v.draft)
		c=MarkerContent.objects.create(marker=m)

		# test creation of ticket
		response = self.client_user1.get(REQUEST_URL.format("marker_content", c.pk))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(ImageFile.objects.count(), 1)
		ticket_id = response.data["ticket_id"]

		# test complete notification
		response = self.client_user1.get(COMPLETE_URL.format(ticket_id))
		self.assertEqual(response.status_code, 200)
