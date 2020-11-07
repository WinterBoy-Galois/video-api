from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.videos.models import MarkerContent

CONTENT_URL = '/v1/markercontent/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_access(self):

        self.setup_users_clients_and_videos()

        # no access without login
        response = self.client.get(CONTENT_URL)
        self.assertEqual(response.status_code, 403)

        # access with login
        response = self.client_user1.get(CONTENT_URL)
        self.assertEqual(response.status_code, 200)

    def test_creation(self):
        self.setup_users_clients_and_videos();

        mid = self.markers[0].pk
        response = self.client_user1.post_json(CONTENT_URL, {"marker":mid})
        self.assertEqual(response.status_code, 201)


    def test_creation_nested_content(self):
        self.setup_users_clients_and_videos();

        mid = self.markers[0].pk
        response = self.client_user1.post_json(CONTENT_URL, {"marker":mid, "content": {"title": "test"} })
        self.assertEqual(response.status_code, 201)

        response = self.client_user1.get(CONTENT_URL + str(response.data['id']) + '/')

        self.assertEqual(response.data['content']['title'], "test")
