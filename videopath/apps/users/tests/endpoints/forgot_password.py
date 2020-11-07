from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

RESET_URL = '/v1/user/me/password-reset/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_post_access(self):
        self.setup_users_and_clients()

        # should get list with one user
        response = self.client.post_json(RESET_URL, {"username": "some name"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post_json(RESET_URL, {"username": self.USER1_DETAILS["username"]})
        self.assertEqual(response.status_code, 201)

        response = self.client.post_json(RESET_URL, {"username": self.USER1_DETAILS["email"]})
        self.assertEqual(response.status_code, 201)

