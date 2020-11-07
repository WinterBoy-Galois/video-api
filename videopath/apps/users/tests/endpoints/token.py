from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

API_URL = '/v1/'
TOKEN_URL = '/v1/api-token/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_access(self):
        self.setup_users_and_clients()

        # should get list with one user
        response = self.client_user1.get_json(TOKEN_URL)
        self.assertEqual(response.status_code, 405)

    def test_login(self):
        self.setup_users_and_clients()

        credentials = {
            'username': self.USER1_DETAILS['username'], 
            'password': self.USER1_DETAILS['password']
            }

        # no login without credentials
        response = self.client.post_json(TOKEN_URL, {})
        self.assertEqual(response.status_code, 403)

        # login with credentials
        response = self.client.post_json(TOKEN_URL, credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("api_token", None))
        self.assertIsNotNone(response.data.get("user", None))
        self.assertIsNotNone(response.data.get("api_token_once", None))


    def test_login_logout(self):
        self.setup_users_and_clients()

        credentials = {
            'username': self.USER1_DETAILS['username'], 
            'password': self.USER1_DETAILS['password']
            }

        # no login should provide no access    
        response = self.client.get_json(API_URL)
        self.assertEqual(response.status_code, 403)

        # login
        response = self.client.post_json(TOKEN_URL, credentials)
        self.assertEqual(response.status_code, 200)
        token = response.data.get("api_token", None)

        # set token and test access again
        self.client.credentials( HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get_json(API_URL)
        self.assertEqual(response.status_code, 200)

        # delete token and try again
        response = self.client.delete(TOKEN_URL)
        self.assertEqual(response.status_code, 200)

        # old token should not work anymore
        response = self.client.get_json(API_URL)
        self.assertEqual(response.status_code, 403)
