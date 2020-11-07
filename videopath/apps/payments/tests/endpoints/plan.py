from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

PLAN_URL = '/v1/plan/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_and_post_access(self):
        self.setup_users_and_clients()

        # there should be some plans to choose from
        response = self.client_user1.get(PLAN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("count")>2)

        # posting should not be allowed
        response = self.client_user1.post_json(PLAN_URL, {})
        self.assertEqual(response.status_code, 405)

