from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

MARKER_URL = '/v1/marker/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_access(self):
        self.setup_users_clients_and_videos();

    	# no access without login
        response = self.client.get(MARKER_URL)
        self.assertEqual(response.status_code, 403)

        # access with login
        response = self.client_user1.get(MARKER_URL)
        self.assertEqual(response.status_code, 200)

    def test_creation(self):
        self.setup_users_clients_and_videos();

        response = self.client_user1.post_json(MARKER_URL, {"video_revision":self.video.draft.pk})
        self.assertEqual(response.status_code, 201)
