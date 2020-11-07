from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

CC_URL = '/v1/user/1/credit-card/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_and_post_access(self):
        self.setup_users_and_clients()

        # should fail as the token is missing
        response = self.client_user1.put_json(CC_URL, {})
        self.assertEqual(response.status_code, 400)

        # should fail as there is no card
        response = self.client_user1.get_json(CC_URL)
        # self.assertEqual(response.status_code, 404)

